#!/bin/bash
#
# NOTE: this script submits GLA.py -- the custom-EA task -- and NOT the NSGA-III
# driver NSGA3_DEAP.py that sits alongside it. GLA.py ignores any arguments
# passed through "$@". It is retained here as the record of how the custom-EA
# experiments were submitted. See the README for details.
#
#$ -cwd
#$ -j y
#$ -q all.q
./GLA.py $@

