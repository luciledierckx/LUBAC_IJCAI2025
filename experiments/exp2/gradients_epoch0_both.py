import os
import torch
import numpy as np
from argparse import ArgumentParser
import time
import multiprocessing as mp
import pandas as pd


from pyschlandals.learner import PyLearner
from pyschlandals.learn import PyLearnParameters, PyLoss, PyLearningMethod, PyApproximateMethod

torch.manual_seed(0)
np.random.seed(0)

def do_experiment(dico):
    dataset = dico["dataset"]
    timeout = dico["timeout"]
    instance = dico["instance"]
    f = dico["f"]
    v = dico["v"]
    
    lr = 0.3
    n_epochs = 1
    jobs = 1

    # Load dataset
    uai = "/experiments/data/"+dataset+".uai"
    output_folder = "/experiments/data/outputs_LDS/bayesian_networks/"+dataset+"/grad_e0_comparison_both/t"+str(timeout)+'/'
    os.makedirs(output_folder, exist_ok=True)
    tmp_f = dataset+"both"+str(timeout)+"tmp"+str(instance)+".csv"

    output_file = output_folder+str(instance+1)+".csv"
    header = "Instance,Proba\n"
    with open(tmp_f, "w") as tmp:
        tmp.writelines([header]+[str(f)+","+str(v)])
    
    params = PyLearnParameters(lr=lr, nepochs=n_epochs, compilation_timeout=timeout, learn_timeout=None, loss=None, 
                            optimizer=None, lr_drop=None, epoch_drop=None, early_stop_threshold=None, early_stop_delta=None, 
                            patience=None, recompile=False, e_weighted=False, equal_init=False)
    
    both = PyLearner(input=uai, params=params, branching=None, outfolder=None, epsilon=None, jobs=jobs,
                    semiring=None, trainfile=tmp_f, testfile=None, learning_m=PyLearningMethod.Both, approx=PyApproximateMethod.LDS)
    print('both', both.evaluate(), both.get_epsilon(0))        
    
    exact_timeout = 1200
    params_full = PyLearnParameters(lr=lr, nepochs=n_epochs, compilation_timeout=exact_timeout, learn_timeout=None, loss=None,
                                    optimizer=None, lr_drop=None, epoch_drop=None, early_stop_threshold=None, early_stop_delta=None,
                                    patience=None, recompile=False, e_weighted=False, equal_init=False)
    exact_start = time.time()
    exact = PyLearner(input=uai, params=params_full, branching=None, outfolder=None, epsilon=None, jobs=jobs,
                    semiring=None, trainfile=tmp_f, testfile=None,learning_m=PyLearningMethod.Models, approx=PyApproximateMethod.Bounds)
    exact_end = time.time()
    
    if len(exact.get_expected())==0:
        os.remove(tmp_f)
        return
    
    with open(output_file, "w") as out:
        out.write("expected,pred_l,pred_u,exact,grad_l,grad_u,grad_exact,weights\n")
    
    pred_both1, _, grad_both1, _ = both.eval_loss_grad([0], None, [both.get_expected()[0]])
    pred_both2, _, grad_both2, _ = both.eval_loss_grad([1], None, [both.get_expected()[1]])
    pred_exact, _, grad_exact, _ = exact.eval_loss_grad(None, None, exact.get_expected())
    
    
    with open(output_file, "a") as out:
        out.write(str(v)+","+'{:.5e}'.format(pred_both1[0])+","+'{:.5e}'.format(pred_both2[0])+","+'{:.5e}'.format(pred_exact[0])+","
                +str(' '.join([' '.join(['{:.5e}'.format(elem) if elem!=0 else str(elem) for elem in v]) for v in grad_both1[0]])+",")
                +str(' '.join([' '.join(['{:.5e}'.format(elem) if elem!=0 else str(elem) for elem in v]) for v in grad_both2[0]]))+','
                +str(' '.join([' '.join(['{:.5e}'.format(elem) if elem!=0 else str(elem) for elem in v]) for v in grad_exact[0]]))+','
                +str(' '.join([' '.join(['{:.5e}'.format(elem) if elem!=0 else str(elem) for elem in v]) for v in both.get_distributions()]))+
                "\n")
            

    os.remove(tmp_f)
        
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--dataset", type=str)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--n_jobs", type=int)
    args = parser.parse_args()
    
    expected = pd.read_csv("/experiments/data/bn_true_probas.csv", header=None)
    munin = expected[expected[0].str.contains(args.dataset)]
    train = pd.read_csv("/experiments/data/train_"+args.dataset+".csv")
    test = pd.read_csv("/experiments/data/test_"+args.dataset+".csv")
    mapping = {}
    cnt_train = 0
    cnt_test = 0
    for i, out in enumerate(munin[1]):
        inst = args.dataset+"/"+str(i+1)+".cnf"
        if out == 0: 
            if train['Proba'][cnt_train] == 0 and test['Proba'][cnt_test] != 0:
                mapping[inst] = (train['Instance'][cnt_train], train['Proba'][cnt_train])
                cnt_train += 1
            elif train['Proba'][cnt_train] != 0 and test['Proba'][cnt_test] == 0:
                mapping[inst] = (test['Instance'][cnt_test], test['Proba'][cnt_test])
                cnt_test += 1
            else:
                mapping[inst] = (train['Instance'][cnt_train], train['Proba'][cnt_train])
                cnt_train += 1
            continue
        if cnt_train< len(train['Proba']) and abs(out - train['Proba'][cnt_train]) < 0.000001:
            mapping[inst] = (train['Instance'][cnt_train], train['Proba'][cnt_train])
            cnt_train += 1
        elif cnt_test<len(test['Proba']) and abs(out - test['Proba'][cnt_test]) < 0.000001:
            mapping[inst] = (test['Instance'][cnt_test], test['Proba'][cnt_test])
            cnt_test += 1

    times_file = '/experiments/data/outputs_LDS/bayesian_networks/'+args.dataset+'/compile_time_dfs.csv'
    dfs_times = pd.read_csv(times_file)
    dico_l = []
    
    for i, k in enumerate(mapping.keys()):
        out =  dfs_times[dfs_times['V1'].str.contains(k)]['Stdout']
        out = out.iloc[0].split(" ")
        e = float(out[-6][:-1])
        t = int(out[-3])
        if t < 590 and e < 0.00001:
            print(e)
            f, v = mapping[k]
            dico = {"dataset": args.dataset, "timeout": args.timeout, "instance": i, "f": f, "v": v}
            dico_l.append(dico)

    pool = mp.Pool(args.n_jobs)
    results = pool.map(do_experiment, dico_l)