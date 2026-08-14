#!/bin/bash

OUTPUT_DIR="/experiments/data/outputs_LDS/bayesian_networks"
DATA_DIR="/experiments/data"


for timeout in 5 50 150
do
    for d in munin water pigs
    do
        parallel --bar "mkdir -p $OUTPUT_DIR/{1}/learning_m/models_t{2}/ && schlandals -t {2} --input $DATA_DIR/{1}.uai --approx lds learn --trainfile $DATA_DIR/train_test_uai/train_{1}.csv --testfile $DATA_DIR/train_test_uai/test_{1}.csv --outfolder $OUTPUT_DIR/{1}/learning_m/models_t{2}/ --nepochs 6000 --do-log --jobs 80 --ltimeout 3600 --learning-m models" ::: $d ::: $timeout
        parallel --bar "mkdir -p $OUTPUT_DIR/{1}/learning_m/both_t{2}/ && schlandals -t {2} --input $DATA_DIR/{1}.uai --approx lds learn --trainfile $DATA_DIR/train_test_uai/train_{1}.csv --testfile $DATA_DIR/train_test_uai/test_{1}.csv --outfolder $OUTPUT_DIR/{1}/learning_m/both_t{2}/ --nepochs 6000 --do-log --jobs 80 --ltimeout 3600 --learning-m both" ::: $d ::: $timeout
        parallel --bar "mkdir -p $OUTPUT_DIR/{1}/learning_m/nonmodels_t{2}/ && schlandals -t {2} --input $DATA_DIR/{1}.uai --approx lds learn --trainfile $DATA_DIR/train_test_uai/train_{1}.csv --testfile $DATA_DIR/train_test_uai/test_{1}.csv --outfolder $OUTPUT_DIR/{1}/learning_m/nonmodels_t{2}/ --nepochs 6000 --do-log --jobs 80 --ltimeout 3600 --learning-m non-models" ::: $d ::: $timeout
    done
done

parallel --bar "mkdir -p $OUTPUT_DIR/{1}/learning_m/models/ && schlandals -t 600 --input $DATA_DIR/{1}.uai learn --trainfile $DATA_DIR/train_test_uai/train_{1}.csv --testfile $DATA_DIR/train_test_uai/test_{1}.csv --outfolder $OUTPUT_DIR/{1}/learning_m/models/ --nepochs 6000 --do-log --jobs 80 --ltimeout 3600 --learning-m models" ::: munin
parallel --bar "mkdir -p $OUTPUT_DIR/{1}/learning_m/models/ && schlandals -t 600 --input $DATA_DIR/{1}.uai learn --trainfile $DATA_DIR/train_test_uai/train_{1}.csv --testfile $DATA_DIR/train_test_uai/test_{1}.csv --outfolder $OUTPUT_DIR/{1}/learning_m/models/ --nepochs 6000 --do-log --jobs 80 --ltimeout 3600 --learning-m models" ::: water
parallel --bar "mkdir -p $OUTPUT_DIR/{1}/learning_m/models/ && schlandals -t 600 --input $DATA_DIR/{1}.uai learn --trainfile $DATA_DIR/train_test_uai/train_{1}.csv --testfile $DATA_DIR/train_test_uai/test_{1}.csv --outfolder $OUTPUT_DIR/{1}/learning_m/models/ --nepochs 6000 --do-log --jobs 80 --ltimeout 3600 --learning-m models" ::: pigs
