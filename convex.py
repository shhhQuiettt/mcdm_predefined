from typing import Any
import numpy.typing as npt
from outranking_relation import OutrankingRelation


def nsga2(
    variants: list[Any], chosen_amount: int, outranking_relation: OutrankingRelation
) -> list[list[Any]]:
    ...
    return [[]]


def chosen_strength(
    subset_indices: npt.NDArray, outranking_relation: OutrankingRelation
) -> float:
    strength = 0
    for chosen_variant_id in range(outranking_relation.no_of_variants):
        if subset_indices[chosen_variant_id] == 0:
            continue

        for rejected_variant_id in range(outranking_relation.no_of_variants):
            if subset_indices[rejected_variant_id] == 1:
                continue

            strength += outranking_relation.preference_over_indeces(
                of=chosen_variant_id, over=rejected_variant_id
            )

    return strength


def rejected_weakness(
    subset_indices: npt.NDArray, outranking_relation: OutrankingRelation
) -> float:
    weakness = 0
    for rejected_id in range(outranking_relation.no_of_variants):
        if subset_indices[rejected_id] == 1:
            continue

        weakness += max(
            (
                outranking_relation.preference_over_indeces(
                    of=chosen_variant_id, over=rejected_id
                )
                for chosen_variant_id in range(outranking_relation.no_of_variants)
                if subset_indices[chosen_variant_id] == 1
            )
        )

    return weakness


def rejected_strength(
    subset_indices: npt.NDArray, outranking_relation: OutrankingRelation
) -> float:
    strength = 0

    for rejected_variant_id in range(outranking_relation.no_of_variants):
        if subset_indices[rejected_variant_id] == 1:
            continue

        for chosen_variant_id in range(outranking_relation.no_of_variants):
            if subset_indices[chosen_variant_id] == 0:
                continue

            strength += outranking_relation.preference_over_indeces(
                of=rejected_variant_id, over=chosen_variant_id
            )

    return strength


def chosen_weakness(
    subset_indices: npt.NDArray, outranking_relation: OutrankingRelation
) -> float:
    max_preferences_rejected_over_chosen = []

    for rejected_variant_id in range(outranking_relation.no_of_variants):
        if subset_indices[rejected_variant_id] == 1:
            continue

        max_preferences_rejected_over_chosen.append(
            max(
                (
                    outranking_relation.preference_over_indeces(
                        of=rejected_variant_id, over=chosen_variant_id
                    )
                )
                for chosen_variant_id in range(outranking_relation.no_of_variants)
                if subset_indices[chosen_variant_id] == 1
            )
        )

    return min(max_preferences_rejected_over_chosen)
