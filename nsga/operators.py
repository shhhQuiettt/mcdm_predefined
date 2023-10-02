from pymoo.core.crossover import Crossover
from pymoo.core.mutation import Mutation

import numpy as np


class BinaryCrossover(Crossover):
    def __init__(self):
        super().__init__(n_parents=2, n_offsprings=1)

    # Take a look again
    def _do(self, problem, X, **kwargs):
        n_parents, n_matings, n_var = X.shape
        print(f"{self.n_offsprings=}, {n_matings=}, {problem.n_var=}")

        _X = np.full((self.n_offsprings, n_matings, problem.n_var), False, dtype=int)

        for k in range(n_matings):
            p1, p2 = X[0, k], X[1, k]

            both_are_true = np.logical_and(p1, p2)
            _X[0, k, both_are_true] = True

            n_remaining = problem.chosen_amount - np.sum(both_are_true)

            I = np.where(np.logical_xor(p1, p2))[0]

            S = I[np.random.permutation(len(I))][:n_remaining]
            _X[0, k, S] = True
            # _X[1] = _X[0].copy()

        return _X


class TwoBitsSwapMutation(Mutation):
    def __init__(self, prob=1.0):
        super().__init__(prob=prob)

    def _do(self, problem, X, **kwargs):
        for i in range(X.shape[0]):
            false_indices = np.where(X[i, :] == False)[0]
            true_indices = np.where(X[i, :] == True)[0]

            # print(f"{false_indices=}")
            # print(f"{true_indices=}")
            # print()

            X[i, np.random.choice(false_indices)] = True
            X[i, np.random.choice(true_indices)] = False

        return X
