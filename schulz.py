from outranking_relation import OutrankingRelation, OutrankingMatrixNumpy
from typing import Iterable, Any
import numpy.typing as npt
import numpy as np
import itertools


def floyd_warshall(distance_matrix: npt.NDArray):
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

    return OutrankingMatrixNumpy(pair_thresholded_matrix, variants)


def schulz(
    variants: list[str], winners_amount: int, outranking_relation: OutrankingRelation
) -> list[str]:
    example = np.array(
        [
            [1, 0.001, 0.527, 0.334],
            [0.772, 1, 0.833, 0.923],
            [0.617, 0.107, 1, 0.313],
            [0.017, 0.821, 0.717, 1],
        ]
    )
    pairwise_preference_matrix = pair_thresholded_preference_matrix(
        list(range(4)), OutrankingMatrixNumpy(example, list(range(4)))
    ).matrix

    print(pairwise_preference_matrix)

    print(floyd_warshall(pairwise_preference_matrix))

    return variants
