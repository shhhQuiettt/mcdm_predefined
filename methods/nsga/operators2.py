from pymoo.core.crossover import Crossover
from pymoo.core.mutation import Mutation
from pymoo.core.sampling import Sampling

import numpy as np


class RandomSubsetSampling(Sampling):
    def _do(self, problem, n_samples, **kwargs):
        X = np.zeros((n_samples, problem.n_var), dtype=int)

        for solution_id in range(n_samples):
            included_variants = np.random.choice(
                range(problem.outranking_relation.no_of_variants),
                problem.chosen_amount,
                replace=False,
            )
            X[solution_id] = included_variants

        X.sort(axis=1)

        return X


class BinaryCrossover(Crossover):
    def __init__(self):
        super().__init__(n_parents=2, n_offsprings=1)

    def _do(self, problem, X, **kwargs):
        n_parents, n_matings, n_var = X.shape

        _X = np.full((self.n_offsprings, n_matings, problem.n_var), 0)

        for k in range(n_matings):
            p1, p2 = X[0, k], X[1, k]
            unique_variants = np.unique(np.concatenate((p1, p2)))

            _X[0, k] = np.random.choice(unique_variants, n_var, replace=False)
            _X[0, k].sort()

        return _X


class TwoBitsSwapMutation(Mutation):
    def _do(self, problem, X, **kwargs):
        for i in range(X.shape[0]):
            while (
                new_element := np.random.choice(
                    range(problem.outranking_relation.no_of_variants)
                )
            ) in X[i]:
                pass

            X[i, np.random.choice(range(problem.chosen_amount))] = new_element
            X[i].sort()

        return X
