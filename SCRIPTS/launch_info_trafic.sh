#! /bin/bash

# add anaconda2 bin dir in path
export PATH="/infres/ir430/bd/stif/anaconda2/bin:$PATH"

# start conda environment
source activate stif

cd /infres/ir430/bd/stif/PYTHON

python info_trafic.py &
