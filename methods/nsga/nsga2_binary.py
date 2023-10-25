from outranking_relation.outranking_relation import OutrankingRelation
from .operators import BinaryCrossover, TwoBitsSwapMutation

from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem
from pymoo.termination import get_termination
from pymoo.optimize import minimize
from pymoo.core.sampling import Sampling
import numpy.typing as npt
import numpy as np


def nsga2(
    variants: list[str], chosen_amount: int, outranking_relation: OutrankingRelation
) -> list[list[str]]:
    problem = ChoosingVariants(outranking_relation, chosen_amount)
    algorithm = NSGA2(
        pop_size=100,
        sampling=RandomSubsetSampling(),
        crossover=BinaryCrossover(),
        mutation=TwoBitsSwapMutation(prob=0.5),
        eliminate_duplicates=True,
        verbose=True,
    )
    res = minimize(
        problem,
        algorithm,
        seed=2137,
        termination=get_termination("n_gen", 100),
        verbose=True,
    )

    chosen_solutions_sets = [
        np.array(variants)[np.where(binary_solution == 1)] for binary_solution in res.X
    ]

    return [
        list(chosen_solutions_set) for chosen_solutions_set in chosen_solutions_sets
    ]


class RandomSubsetSampling(Sampling):
    def _do(self, problem, n_samples, **kwargs):
        X = np.full((n_samples, problem.n_var), False, dtype=bool)
        for solution_id in range(n_samples):
            included_variants_id = np.random.choice(
                problem.n_var, problem.chosen_amount, replace=False
            )

            X[solution_id, included_variants_id] = True

        return X


class ChoosingVariants(ElementwiseProblem):
    def __init__(
        self, outranking_relation: OutrankingRelation, chosen_amount: int
    ) -> None:
        self.outranking_relation = outranking_relation
        self.chosen_amount = chosen_amount
        super().__init__(
            n_var=outranking_relation.no_of_variants,
            n_obj=4,
            # n_eq_constr=1,
            n_ieq_constr=1,
        )

    def _evaluate(self, solution, out, *args, **kwargs):
        out["F"] = [
            -self.chosen_strength(solution),
            -self.rejected_weakness(solution),
            self.rejected_strength(solution),
            self.chosen_weakness(solution),
        ]

        # constraint equals 0 (valid solution) only if the sum of chosen variants is equal to the chosen amount
        out["G"] = (self.chosen_amount - sum(solution)) ** 2

    def chosen_strength(self, subset_indices: npt.NDArray) -> float:
        strength = 0
        for chosen_variant_id in range(self.outranking_relation.no_of_variants):
            if subset_indices[chosen_variant_id] == 0:
                continue

            for rejected_variant_id in range(self.outranking_relation.no_of_variants):
                if subset_indices[rejected_variant_id] == 1:
                    continue

                strength += self.outranking_relation.preference_over_indeces(
                    of=chosen_variant_id, over=rejected_variant_id
                )

        return strength

    def rejected_weakness(self, subset_indices: npt.NDArray) -> float:
        weakness = 0
        for rejected_id in range(self.outranking_relation.no_of_variants):
            if subset_indices[rejected_id] == 1:
                continue

            weakness += max(
                (
                    self.outranking_relation.preference_over_indeces(
                        of=chosen_variant_id, over=rejected_id
                    )
                    for chosen_variant_id in range(
                        self.outranking_relation.no_of_variants
                    )
                    if subset_indices[chosen_variant_id] == 1
                )
            )

        return weakness

    def rejected_strength(self, subset_indices: npt.NDArray) -> float:
        strength = 0

        for rejected_variant_id in range(self.outranking_relation.no_of_variants):
            if subset_indices[rejected_variant_id] == 1:
                continue

            for chosen_variant_id in range(self.outranking_relation.no_of_variants):
                if subset_indices[chosen_variant_id] == 0:
                    continue

                strength += self.outranking_relation.preference_over_indeces(
                    of=rejected_variant_id, over=chosen_variant_id
                )

        return strength

    def chosen_weakness(self, subset_indices: npt.NDArray) -> float:
        max_preferences_rejected_over_chosen = []

        for rejected_variant_id in range(self.outranking_relation.no_of_variants):
            if subset_indices[rejected_variant_id] == 1:
                continue

            max_preferences_rejected_over_chosen.append(
                max(
                    (
                        self.outranking_relation.preference_over_indeces(
                            of=rejected_variant_id, over=chosen_variant_id
                        )
                    )
                    for chosen_variant_id in range(
                        self.outranking_relation.no_of_variants
                    )
                    if subset_indices[chosen_variant_id] == 1
                )
            )

        return min(max_preferences_rejected_over_chosen)
