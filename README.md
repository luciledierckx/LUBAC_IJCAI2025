# Learning from Logical Constraints with Lower- and Upper-Bound Arithmetic Circuits

This repository contains the code that was used for the experiments of the paper ["Learning from Logical Constraints with Lower- and Upper-Bound Arithmetic Circuits"](https://www.ijcai.org/proceedings/2025/0558.pdf) published at IJCAI in 2025. 

## Abstract of Paper

An important class of neuro-symbolic (NeSy) methods relies on knowledge compilation (KC) techniques to transform logical constraints into a differentiable exact arithmetic circuit (AC) that represents all models of a logical formula. However, given the complexity of KC, compiling such exact circuits can be infeasible. Previous works in such cases proposed to compile a circuit for a subset of models. In this work, we will show that gradients calculated on a subset of models can be very far from true gradients. We propose a new framework that calculates gradients based on compiling logical constraints partially in not only a lower-bound circuit but also an upper-bound circuit. We prove that from this pair of ACs, gradients that are within a bounded distance from true gradients can be calculated. Our experiments show that adding the upperbound AC also helps the learning process in practice, allowing for similar or better generalisation than working solely with fully compiled ACs, even with less than 150 seconds of partial compilation.

## Repository Structure

```
.
├── src/                # Schlandals solver source (Rust)
│   ├── solver.rs        # Main contribution: LUBAC compilation logic
│   └── learning/
│       └── learner.rs   # Main contribution: learning with lower/upper bound ACs
├── pyschlandals/       # Python bindings for Schlandals
├── experiments/        # Scripts and notebooks used to produce the paper's results
│   ├── data/             # Input datasets and precomputed outputs
│   ├── exp1/             # How well does LUBAC learning generalise?
│   ├── exp2/             # How are the initial gradients impacted by which AC is used?
│   └── exp3/             # What is the time overhead to compile both lower- and upper-bound ACs?
├── tests/               # Integration tests and CNF test instances
├── doc/                 # Schlandals documentation source (mdBook)
└── LICENSE
```

## LUBAC Code

The code for the compilation of a lower- and upper-bound arithmetic circuit was originally implemented in a branch of the Schlandals solver, available and updated on the [Schlandals repository](https://github.com/aia-uclouvain/schlandals). For accesibility purposes, it is also included here, along with the code to run the experiments of the paper. The main contributions to the Schlandals code are located in `src/solver.rs` and `src/learning/learner.rs`. 

> **Note:** the version of Schlandals in this repository is a snapshot corresponding to the one used for the paper's experiments, and may differ from the latest version available in the main Schlandals repository.

## Installation

For installation instructions (Rust toolchain, system dependencies, build steps), please refer to the [Schlandals Installation Guide](https://aia-uclouvain.github.io/schlandals/install.html).

Python bindings for Schlandals are available in [`pyschlandals/`](pyschlandals/). To build and use them:

```bash
cd pyschlandals/src
maturin develop
```

See [`pyschlandals/example`](pyschlandals/example) for minimal usage examples (`compile.py`, `simple.py`, `train.py`).

## Running the Experiments

All experiment code is located in the `experiments/` folder. Datasets were downloaded from the [BNLearn repository](https://www.bnlearn.com/bnrepository/) and are provided pre-processed in `experiments/data/`.

### Experiment 1 — How well does LUBAC learning generalise?

```bash
cd experiments/exp1
bash exp1.sh
```

Saves the learning generalisation on a test set for each dataset with different compilation timeouts and AC types.

### Experiment 2 — How are the initial gradients impacted by which AC is used?

```bash
cd experiments/exp2
bash epoch0_both.sh       
bash epoch0_models.sh     
bash epoch0_nonmodels.sh  
```

Results can be inspected in `grad_epoch0.ipynb`.

### Experiment 3 — What is the time overhead to compile both lower- and upper-bound ACs?

Open and run `compilation_time_new_compilation.ipynb`. Here the compilation time are already mesured in csv files as it requires to modify the code to measure the initial compilation time. The notebook will generate the plots for the paper.

## About Schlandals

[Schlandals](https://github.com/aia-uclouvain/schlandals) is a state-of-the-art *Projected Weighted Model Counter* specialized for probabilistic inference over discrete probability distributions. Currently, it supports modelization for the following problems:

- Computing the marginal probabilities of a variable in a Bayesian Network
- Computing the probability that two nodes are connected in a probabilistic graph
- Computing the probability of [ProbLog](https://github.com/ML-KULeuven/problog) programs

For more information on how to use Schlandals and its mechanics, check [the documentation](https://aia-uclouvain.github.io/schlandals).

## License

This project is licensed under the terms of the [LICENSE](LICENSE) file included in this repository.

## Citing

If you use Schlandals, please cite:

```bibtex
@InProceedings{schlandals,
  author    = {Dubray, Alexandre and Schaus, Pierre and Nijssen, Siegfried},
  title     = {{Probabilistic Inference by Projected Weighted Model Counting on Horn Clauses}},
  booktitle = {29th International Conference on Principles and Practice of Constraint Programming (CP 2023)},
  year      = {2023},
  doi       = {10.4230/LIPIcs.CP.2023.15},
}
```

If you use the LDS-based approximation, please also cite:

```bibtex
@InProceedings{schlandals_anytime_approximation,
  author    = {Dubray, Alexandre and Schaus, Pierre and Nijssen, Siegfried},
  title     = {{Anytime Weighted Model Counting With Approximation Guarantees For Probabilistic Inference}},
  booktitle = {30th International Conference on Principles and Practice of Constraint Programming (CP 2024)},
  year      = {2024},
}
```

If you use the lower- and upper-bound arithmetic circuit (LUBAC) compilation method, please cite:

```bibtex
@InProceedings{ijcai2025_lubac,
  author    = {Dierckx, Lucile and Dubray, Alexandre and Nijssen, Siegfried},
  title     = {{Learning from Logical Constraints with Lower- and Upper-Bound Arithmetic Circuits}},
  booktitle = {24th International Joint Conference on Artificial Intelligence (IJCAI 2025)},
  year      = {2025},
}
```