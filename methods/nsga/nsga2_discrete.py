from pandas.core.interchange.dataframe_protocol import enum
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem
from pymoo.termination import get_termination
from pymoo.optimize import minimize
from outranking_relation.outranking_relation import OutrankingRelation
import numpy.typing as npt

from .operators2 import BinaryCrossover, TwoBitsSwapMutation, RandomSubsetSampling

import numpy as np


def nsga2(
    variants: list[str], chosen_amount: int, outranking_relation: OutrankingRelation
) -> list[tuple[list[str], list[float]]]:
    problem = ChoosingVariants(outranking_relation, chosen_amount)
    algorithm = NSGA2(
        pop_size=100,
        sampling=RandomSubsetSampling(),
        crossover=BinaryCrossover(),
        mutation=TwoBitsSwapMutation(),
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
        (list(np.array(variants)[elements_ids]), list(res.F[i]))
        for i, elements_ids in enumerate(res.X)
    ]

    return chosen_solutions_sets


class ChoosingVariants(ElementwiseProblem):
    def __init__(
        self, outranking_relation: OutrankingRelation, chosen_amount: int
    ) -> None:
        self.outranking_relation = outranking_relation
        self.chosen_amount = chosen_amount
        super().__init__(
            n_var=chosen_amount,
            n_obj=4,
        )

    def _evaluate(self, solution, out, *args, **kwargs):
        out["F"] = [
            -self.chosen_strength(solution),
            -self.rejected_weakness(solution),
            self.rejected_strength(solution),
            self.chosen_weakness(solution),
        ]

    def chosen_strength(self, subset: npt.NDArray) -> float:
        strength = 0
        for chosen_variant_id in subset:
            for rejected_variant in range(self.outranking_relation.no_of_variants):
                if rejected_variant in subset:
                    continue

                strength += self.outranking_relation.preference_over_indeces(
                    of=chosen_variant_id, over=rejected_variant
                )

        return strength

    def rejected_weakness(self, subset_indices: npt.NDArray) -> float:
        weakness = 0
        for rejected_id in range(self.outranking_relation.no_of_variants):
            if rejected_id in subset_indices:
                continue
            weakness += max(
                (
                    self.outranking_relation.preference_over_indeces(
                        of=chosen_variant_id, over=rejected_id
                    )
                    for chosen_variant_id in subset_indices
                )
            )

        return weakness

    def rejected_strength(self, subset_indices: npt.NDArray) -> float:
        strength = 0

        for rejected_variant_id in range(self.outranking_relation.no_of_variants):
            for chosen_variant_id in subset_indices:
                if rejected_variant_id in subset_indices:
                    continue

                strength += self.outranking_relation.preference_over_indeces(
                    of=rejected_variant_id, over=chosen_variant_id
                )

        return strength

    def chosen_weakness(self, subset_indices: npt.NDArray) -> float:
        max_preferences_rejected_over_chosen = []

        for rejected_variant_id in range(self.outranking_relation.no_of_variants):
            if rejected_variant_id in subset_indices:
                continue

            max_preferences_rejected_over_chosen.append(
                max(
                    (
                        self.outranking_relation.preference_over_indeces(
                            of=rejected_variant_id, over=chosen_variant_id
                        )
                    )
                    for chosen_variant_id in subset_indices
                )
            )

        return min(max_preferences_rejected_over_chosen)
