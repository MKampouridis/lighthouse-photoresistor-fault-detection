#!/usr/bin/env python3

import os
import sys

# The EA/GA framework this task builds on lives outside this repository (see the
# "Known gaps" section of the README). Point EA_FRAMEWORK_PATH at your checkout.
sys.path.append(os.environ.get('EA_FRAMEWORK_PATH', '../EA'))

# OneMax PROBLEM IMPLEMENTATION. ESSENTIALLY THE ONLY THING WE NEED TO DO IS DEFINE THE PROBLEM-SPECIFIC FITNESS
# FUNCTION. ALL OTHER GA FUNCTIONS (E.G. CROSSOVER, MUTATION) ARE WRITTEN IN THE PARENT CLASSES EA AND GA. WE CAN OF
# COURSE OVER-WRITE THEM HERE, IF WE WANT A DIFFERENT IMPLEMENTATION, E.G. A DIFFERENT CROSSOVER OPERATOR.
from EA import Problem
from GA.GA import GA
from random import seed
import drifted_analysis_for_GA as da

seed(111)  # Using a seed for reproducibility purposes, as GA is a stochastic algorithm.
nRUNS = 5
POPULATION_SIZE = 2500
nGENS = 5  # Number of generations
GENES = len(da.features_all) # 10  # Number of genes (cells) in each chromosome
XOVER_PROB = 0.75
TOURNAMENT_SIZE = 4
GENES_TYPE = "int"  # Define the type of the GA genes, if e.g. they will be int or float
LB = 0  # Lower boundary (inclusive) of the potential gene values that are generated
UB = 1  # Upper boundary (inclusive) of the potential gene values that are generated
PROBLEM = Problem.MINIMISATION  # Setup as maximisation problem


class GLA(GA):

    def __init__(self):
        super().__init__(type_of_genes=GENES_TYPE, lower_bound=LB, upper_bound=UB, pop_size=POPULATION_SIZE,
                         no_of_genes=GENES, problem=PROBLEM)

    # Fitness function: sum of genes. The dataset and flag argument is not needed in the OneMax problem.
    def evaluate(self, individual, dataset=None, flag=None):
        individual.fitness = da.check_drifting(individual.model)


# Runs the EA algorithm over a number of independent runs and prints and saves results.
if __name__ == '__main__':
    task = GLA()
    task.run(population_size=POPULATION_SIZE, xover_prob=XOVER_PROB, tournament_size=TOURNAMENT_SIZE,
             no_of_gens=nGENS, no_of_runs=nRUNS, training_dataset=None, test_dataset=None,
             class_object=GLA.Individual(""))
