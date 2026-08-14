for dataset in 'water' 'pigs' 'munin'
do
    for t in 5 50 150 
    do
        python3.9 ./gradients_epoch0_nonmodels.py --dataset $dataset --t $t --n_jobs 80
    done
done
