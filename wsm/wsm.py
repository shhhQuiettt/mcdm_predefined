from typing import Any, Callable

import os

from .objectives import (
    chosen_strength,
    rejected_weakness,
    rejected_strength,
    chosen_weakness,
)
from outranking_relation import OutrankingRelation
import numpy.typing as npt
from outranking_relation import OutrankingRelation
import numpy as np
from functools import partial
import itertools


def calculate_objectives(
    objective_functions: list[Callable], possible_subsets: list[tuple[Any]]
):
    CACHE_FILE_NAME = "cache.npy"
    if os.path.isfile(CACHE_FILE_NAME):
        print("Loading from cache...")
        subsets_objectives = np.load(CACHE_FILE_NAME)
        return subsets_objectives

    print("Calculating objectives...")
    subsets_objectives = np.array(
        [
            [objective_function(subset) for objective_function in objective_functions]
            # for subset in random.sample(possible_subsets, 500)
            for subset in possible_subsets
        ]
    )
    np.save(CACHE_FILE_NAME, subsets_objectives)
    print("Saved to cache!")
    return subsets_objectives


def min_max_normalization(
    subsets_objectives: npt.NDArray, objective_function_is_cost: list[bool]
) -> npt.NDArray:
    normalized_subsets_objectives = np.empty_like(subsets_objectives)
    for i in range(normalized_subsets_objectives.shape[1]):
        x = subsets_objectives[:, i]

        if np.min(x) == np.max(x):
            normalized_subsets_objectives[:, i] = np.ones(x.shape)

        if objective_function_is_cost[i]:
            normalized_subsets_objectives[:, i] = (np.max(x) - x) / (
                np.max(x) - np.min(x)
            )
        else:
            normalized_subsets_objectives[:, i] = (x - np.min(x)) / (
                np.max(x) - np.min(x)
            )

    return normalized_subsets_objectives


def wsm_variants(
    variants: list[Any], chosen_amount: int, outranking_relation: OutrankingRelation
) -> list[tuple[Any]]:
    objective_functions = [
        chosen_strength,
        rejected_weakness,
        rejected_strength,
        chosen_weakness,
    ]
    objective_function_is_cost = [False, False, True, True]

    weights_vectors = evenly_spaced_weights(30)
    print(len(weights_vectors))

    optimized_objective_functions = [
        partial(
            objective_function,
            outranking_relation=outranking_relation,
            variants=variants,
        )
        for objective_function in objective_functions
    ]

    possible_subsets = list(itertools.combinations(variants, chosen_amount))

    subsets_objectives = calculate_objectives(
        optimized_objective_functions,
        possible_subsets,
    )

    normalized_subsets_objectives = min_max_normalization(
        subsets_objectives, objective_function_is_cost
    )

    pareto_front = set()
    for weights_vector in weights_vectors:
        wsm_scores = np.sum(normalized_subsets_objectives * weights_vector, axis=1)
        max_score_index = np.argmax(wsm_scores)
        pareto_front.add(max_score_index)

    print(pareto_front)

    result = [possible_subsets[i] for i in pareto_front]

    for i in pareto_front:
        print(possible_subsets[i])
        print(subsets_objectives[i])
        print(normalized_subsets_objectives[i])

    return result


def evenly_spaced_weights(n: int) -> npt.NDArray:
    # Create evenly spaced values for the first three elements
    evenly_spaced_values = np.linspace(0, 1, n + 1)

    # Initialize an empty NumPy array to store the vectors
    vectors = np.empty((0, 4))

    # Iterate through the evenly spaced values for the first three elements
    for val1 in evenly_spaced_values:
        for val2 in evenly_spaced_values:
            for val3 in evenly_spaced_values:
                # Calculate the fourth element to ensure the sum is 1
                val4 = 1 - (val1 + val2 + val3)

                # Check if all values are non-negative
                if val4 > 0 and val3 > 0 and val2 > 0 and val1 > 0:
                    # Append the vector to the NumPy array
                    vectors = np.vstack((vectors, [val1, val2, val3, val4]))

    # Display the vectors
    return vectors
