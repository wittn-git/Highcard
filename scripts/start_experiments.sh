#!/bin/bash

mkdir -p experiments/results
mkdir -p experiments/renders

if [ -z ${VIRTUAL_ENV} ]; then 
    source venv/bin/activate
fi

python3 -m experiments.src.main