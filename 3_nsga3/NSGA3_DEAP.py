import sys
from math import factorial

#import pymop
from deap import base, creator, tools, algorithms
import random
import numpy as np
import pandas as pd
from deap.algorithms import varOr, varAnd
#from pandas.core import algorithms
from math import factorial
from pymop.problem import Problem
#from pymop import factory
import drifted_analysis_for_GA as da

def comb(n, k):
    return factorial(n) // (factorial(k) * factorial(n - k))

NOBJ = 0

station = sys.argv[1]
first_values = sys.argv[2].lower() in ['true', '1', 't', 'y', 'yes']
if station == "NLB":
    if first_values is True:
        NOBJ = 16
    else:
        NOBJ = 8
else:
    if first_values is True:
        NOBJ = 14
    else:
        NOBJ = 7


class NSGA3_DEAP:
    def __init__(self, station, first_values):
        da.setup_module(station, first_values)

setup = NSGA3_DEAP(station, first_values)

K = 10
NDIM = len(da.features_all)  # number of features  # NOBJ + K - 1
P = [5, 4]
SCALES = [1, 0.5]
H_boundary = comb(P[0] + NOBJ - 1, NOBJ - 1)
H_inside = NOBJ
H = H_boundary + H_inside
# H = factorial(NOBJ + P - 1) / (factorial(P) * factorial(NOBJ - 1))
BOUND_LOW, BOUND_UP = 0.0, 1.0


class MyCustomProblem(Problem):
    def __init__(self, n_var):
        super().__init__(n_var=n_var, n_obj=NOBJ, n_constr=0, type_var=int)
        self.xl = np.zeros(n_var)  # Lower bounds of variables
        self.xu = np.ones(n_var)  # Upper bounds of variables

    def _evaluate(self, x, out, *args, **kwargs):
        f = da.check_drifting(x.flatten().tolist())
        out["F"] = np.array(f).reshape(1, len(f))


n_var = NDIM
PROBLEM = MyCustomProblem(n_var)

# ---------------------------------------------------------------------------
# NOTE ON REPRODUCING THE PAPER
#
# The settings below are those of a different experimental run, not the
# configuration reported in the paper. The published NSGA-III setup (paper,
# Section 4) is:
#
#     MU = LAMBDA = 300
#     NGEN  = 35
#     CXPB  = 0.9
#     MUTPB = 0.1
#
# Substitute those four values to reproduce the published results. The lines
# are left as-run rather than back-edited, so that this file remains an
# accurate record of the experiment it was used for.
# ---------------------------------------------------------------------------

# We're using (μ + λ) EA strategy (former being parent population, and latter being offspring population)
MU = int(H + (4 - H % 4))
LAMBDA = MU  # number of children to be produced during crossover and mutation
NGEN = 50
CXPB = .85
MUTPB = .15

# ref_points = tools.uniform_reference_points(NOBJ, P)
# Create, combine and removed duplicates
ref_points = [tools.uniform_reference_points(NOBJ, p, s) for p, s in zip(P, SCALES)]
ref_points = np.concatenate(ref_points, axis=0)
_, uniques = np.unique(ref_points, axis=0, return_index=True)
ref_points = ref_points[uniques]

creator.create("FitnessMulti", base.Fitness, weights=(-1.0,) * NOBJ)
creator.create("Individual", list, fitness=creator.FitnessMulti)


def uniform(low, up, size=None):
    try:
        return [random.uniform(a, b) for a, b in zip(low, up)]
    except TypeError:
        return [random.uniform(a, b) for a, b in zip([low] * size, [up] * size)]


toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, BOUND_LOW,
                 BOUND_UP)  # toolbox.register("attr_float", uniform, BOUND_LOW, BOUND_UP, NDIM)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool,
                 NDIM)  # toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_int)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", PROBLEM.evaluate, return_values_of=["F"])
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.125)
toolbox.register("select", tools.selNSGA3, ref_points=ref_points)


def print_pareto_front(population):
    pareto_fronts = tools.sortNondominated(population, len(population), first_front_only=True)
    pareto_front = pareto_fronts[0]

    # Print the Pareto front
    print("Pareto Front:")
    print('Length: ', len(pareto_front))
    for ind in pareto_front:
        print(ind, ind.fitness.values)


def main(seed=None):
    random.seed(seed)

    # Initialize statistics object
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean, axis=0)
    stats.register("std", np.std, axis=0)
    stats.register("min", np.min, axis=0)
    stats.register("max", np.max, axis=0)

    logbook = tools.Logbook()
    logbook.header = "gen", "evals", "std", "min", "avg", "max"

    pop = toolbox.population(n=MU)

    ####################################################################################################################
    #### The following lines of code are if I want to inject into the initial population some specific individuals #####
    #### I should remove / comment the following lines if I want a completely random  initial population ###############
    ####################################################################################################################
    #file_path = 'initial_pop.csv'
    #df = pd.read_csv(file_path, header=None, dtype=int)
    #population_from_csv = [row.tolist() for index, row in df.iterrows()]
    #initial_population = [creator.Individual(ind) for ind in population_from_csv]

    #file_path = 'initial_pop_fitness.csv'
    #df = pd.read_csv(file_path, header=None)
    #fitness_values = [row.tolist() for index, row in df.iterrows()]
    ## Assign fitness values to each individual in the population
    #for ind, fit_vals in zip(initial_population, fitness_values):
    #    ind.fitness.values = tuple(fit_vals)

    #if len(initial_population) < len(pop):
    #    pop[:len(initial_population)] = initial_population
    #elif len(initial_population) == len(pop):
    #    pop[:] = initial_population
    #else:
    #    print('SHOULD NEVER REACH HERE!!!!')
    #    sys.exit()
    ####################################################################################################################
    ####################################################################################################################

    # Evaluate the individuals with an invalid fitness. An invalid fitness is a boolean that indicates whether the
    # fitness has been calculated already. If I've injected individuals in the lines above, then fitness below will not
    # be re-calculated.
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit
        # print(ind, ind.fitness)

    # Compile statistics about the population
    record = stats.compile(pop)
    logbook.record(gen=0, evals=len(invalid_ind), **record)
    print(logbook.stream)

    print_pareto_front(pop)

    # Begin the generational process
    for gen in range(1, NGEN):
        offspring = varOr(pop, toolbox, LAMBDA, CXPB, MUTPB)

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        counter = 0
        # for ind in invalid_ind:
        #     if counter == 277 or counter == 278:
        #         fit = toolbox.evaluate(ind)
        #     print("Current individual that has finished being evaluated: ", counter)
        #     counter +=1
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
            print("Current individual that has finished being evaluated: ", counter)
            counter += 1

        # Select the next generation population from parents and offspring
        pop = toolbox.select(pop + offspring, MU)
        print_pareto_front(pop)

        # Compile statistics about the new population
        record = stats.compile(pop)
        logbook.record(gen=gen, evals=len(invalid_ind), **record)
        print(logbook.stream)

    return pop, logbook


if __name__ == '__main__':
    main()
