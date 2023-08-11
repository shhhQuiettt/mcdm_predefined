from dataclasses import dataclass
import itertools
import math
import numpy as np
import numpy.typing as npt
import pandas as pd
from enum import Enum


class CriterionType(Enum):
    COST = 1
    GAIN = 2


@dataclass(kw_only=True)
class Criterion:
    name: str
    criterion_type: CriterionType
    weight: float
    indifference_threshold: float
    preference_threshold: float
    veto_threshold: float = math.inf


def get_outranking_relation(
    variants: pd.DataFrame, criterions: list[Criterion]
) -> npt.ArrayLike:
    if not set(c.name for c in criterions).issubset(set(variants.columns)):
        raise ValueError(
            f"Not all criterions are in variants table. Criterions: {[c.name for c in  criterions]}, variants: {variants.columns}"
        )

    comprehensive_concordance_index = get_comprahensive_concordance_index(
        variants, criterions
    )

    marginal_discordance_matrices = [
        marginal_discordance_index(variants, criterion) for criterion in criterions
    ]

    return comprehensive_concordance_index


def get_comprahensive_concordance_index(
    variants: pd.DataFrame, criterions: list[Criterion]
):
    comprehensive_concordance_index = np.zeros((len(variants), len(variants)))

    marginal_concordane_matrices = []
    for criterion in criterions:
        marginal_concordane_matrices.append(
            get_marginal_concordance_index(variants, criterion)
        )

    for criterion, marginal_concordance_index in zip(
        criterions, marginal_concordane_matrices
    ):
        comprehensive_concordance_index += criterion.weight * marginal_concordance_index

    comprehensive_concordance_index /= sum(criterion.weight for criterion in criterions)

    return comprehensive_concordance_index


def get_marginal_concordance_index(
    variants: pd.DataFrame, criterion: Criterion
) -> npt.NDArray:
    if criterion.name not in variants.columns:
        raise ValueError(f"Criterion {criterion.name} is not in variants table")

    marginal_concordance_index = np.zeros((len(variants), len(variants)))
    for variant1, variant2 in itertools.product(variants.index, variants.index):
        marginal_concordance_index[variant1, variant2] = get_marginal_preference(
            variants.loc[variant1], variants.loc[variant2], criterion
        )

    return marginal_concordance_index


def get_marginal_preference(
    variant1: pd.Series, variant2: pd.Series, criterion: Criterion
) -> float:
    if criterion.criterion_type == CriterionType.GAIN:
        if (
            variant2.loc[criterion.name]
            < variant1.loc[criterion.name] + criterion.indifference_threshold
        ):
            return 1
        elif (
            variant2.loc[criterion.name]
            > variant1.loc[criterion.name] + criterion.preference_threshold
        ):
            return 0
        else:
            return (
                (
                    (variant1.loc[criterion.name] + criterion.preference_threshold)
                    - variant2.loc[criterion.name]
                )
            ) / (criterion.preference_threshold - criterion.indifference_threshold)

    elif criterion.criterion_type == CriterionType.COST:
        if (
            variant2.loc[criterion.name]
            > variant1.loc[criterion.name] - criterion.indifference_threshold
        ):
            return 1
        elif (
            variant2.loc[criterion.name]
            < variant1.loc[criterion.name] - criterion.preference_threshold
        ):
            return 0
        else:
            return (
                (variant1.loc[criterion.name] - criterion.preference_threshold)
                - variant2.loc[criterion.name]
            ) / (criterion.indifference_threshold - criterion.preference_threshold)

    else:
        raise ValueError("Unknown criterion type")


def marginal_discordance_index(
    variants: pd.DataFrame, criterion: Criterion
) -> npt.NDArray:
    marginal_discordance_index = np.zeros((len(variants), len(variants)))
    for variant1, variant2 in itertools.product(variants.index, variants.index):
        marginal_discordance_index[variant1, variant2] = get_discordance(
            variants.loc[variant1], variants.loc[variant2], criterion
        )

    return marginal_discordance_index


def get_discordance(
    variant1: pd.Series, variant2: pd.Series, criterion: Criterion
) -> float:
    if criterion.criterion_type == CriterionType.GAIN:
        if (
            variant2.loc[criterion.name]
            > variant1.loc[criterion.name] + criterion.veto_threshold
        ):
            return 1
        elif (
            variant2.loc[criterion.name]
            < variant1.loc[criterion.name] + criterion.preference_threshold
        ):
            return 0

        else:
            return (
                variant2.loc[criterion.name]
                - (variant1.loc[criterion.name] + criterion.preference_threshold)
            ) / (criterion.veto_threshold - criterion.preference_threshold)

    elif criterion.criterion_type == CriterionType.COST:
        if (
            variant2.loc[criterion.name]
            < variant1.loc[criterion.name] - criterion.veto_threshold
        ):
            return 1
        elif (
            variant2.loc[criterion.name]
            > variant1.loc[criterion.name] - criterion.preference_threshold
        ):
            return 0
        else:
            return (
                variant2.loc[criterion.name]
                - (variant1.loc[criterion.name] - criterion.veto_threshold)
            ) / (criterion.veto_threshold - criterion.preference_threshold)

        raise ValueError("Unknown criterion type")
