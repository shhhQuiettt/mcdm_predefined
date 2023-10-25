from outranking_relation.outranking_relation import OutrankingRelation
from typing import Any, Optional
import numpy.typing as npt
import numpy as np
import itertools


def schulz(
    variants: list[str], chosen_amount: int, outranking_relation: OutrankingRelation
) -> list[list[Any]]:
    pairwise_preference_matrix = pair_thresholded_preference_matrix(
        variants, outranking_relation
    )
    paths_strengths = strongest_paths(pairwise_preference_matrix)

    solutions = schulz_iteration(paths_strengths, [], chosen_amount)

    return [[variants[variant_id] for variant_id in solution] for solution in solutions]


def schulz_iteration(
    path_strenghts_matrix: npt.NDArray,
    solution: list[Any],
    desired_length: int,
    depth: int = 0,
):
    # assert len(outranking_variants_ids) == 1, "Current dummy version"

    if len(solution) == desired_length:
        return [solution]

    outranking_variants_ids = get_stongest_path_variant_ids(
        path_strenghts_matrix, solution
    )

    solutions = []
    for chosen_variant_id in outranking_variants_ids:
        new_paths_strengths_matrix = path_strenghts_matrix.copy()
        new_paths_strengths_matrix[chosen_variant_id, :] = 0
        new_paths_strengths_matrix[:, chosen_variant_id] = 0

        new_solution = solution.copy()
        new_solution.append(chosen_variant_id)

        solutions.extend(
            schulz_iteration(
                new_paths_strengths_matrix,
                new_solution,
                desired_length,
                depth=depth + 1,
            )
        )

    return solutions


def strongest_paths(distance_matrix: npt.NDArray) -> npt.NDArray:
    path_strenghs = distance_matrix.copy()

    no_of_vertices = distance_matrix.shape[0]

    for through_id in range(no_of_vertices):
        for from_id in range(no_of_vertices):
            for to_id in range(no_of_vertices):
                if from_id == to_id:
                    continue

                path_strenghs[from_id, to_id] = max(
                    path_strenghs[from_id, to_id],
                    min(
                        path_strenghs[from_id, through_id],
                        path_strenghs[through_id, to_id],
                    ),
                )

    return path_strenghs


def pair_thresholded_preference_matrix(
    variants: list[Any], outranking_relation: OutrankingRelation
):
    pair_thresholded_matrix = np.zeros((len(variants), len(variants)))
    no_of_variants = len(variants)

    for variant1_id, variant2_id in itertools.combinations(range(no_of_variants), 2):
        if outranking_relation.preference(
            variants[variant1_id], variants[variant2_id]
        ) > outranking_relation.preference(
            variants[variant2_id], variants[variant1_id]
        ):
            pair_thresholded_matrix[
                variant1_id, variant2_id
            ] = outranking_relation.preference(
                variants[variant1_id], variants[variant2_id]
            )

        else:
            pair_thresholded_matrix[
                variant2_id, variant1_id
            ] = outranking_relation.preference(
                variants[variant2_id], variants[variant1_id]
            )

    return pair_thresholded_matrix


# This function will break if there are two winning wariatns
# Because it requires that wariants beats ALL converse paths
def get_stongest_path_variant_ids(
    pairwise_preference_matrix: npt.NDArray, already_chosen: Optional[list[int]] = None
) -> list[int]:
    if already_chosen is None:
        already_chosen = []

    no_of_variants = pairwise_preference_matrix.shape[0]

    variants_ids = [
        True if i not in already_chosen else False for i in range(no_of_variants)
    ]

    for variant_id in range(len(variants_ids)):
        if not variants_ids[variant_id]:
            continue

        for other_variant_id in range(len(variants_ids)):
            if not variants_ids[other_variant_id]:
                continue

            if variant_id == other_variant_id:
                continue

            if (
                pairwise_preference_matrix[variant_id, other_variant_id]
                <= pairwise_preference_matrix[other_variant_id, variant_id]
            ):
                variants_ids[variant_id] = False
                break

    return [
        variant_id
        for variant_id in range(len(variants_ids))
        if variants_ids[variant_id]
    ]
