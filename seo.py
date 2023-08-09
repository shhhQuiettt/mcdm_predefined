from typing import Iterable
from outranking_relation import OutrankingRelation
import itertools
import math


def seo_measure(
    chosen_variants: Iterable[str],
    rejected_variants: Iterable[str],
    outranking_relation: OutrankingRelation,
) -> float:
    return min(
        outranking_relation.preference(chosen, rejected)
        for chosen, rejected in itertools.product(chosen_variants, rejected_variants)
    )


def seo(
    variants: list[str], winners_amount: int, outranking_relation: OutrankingRelation
) -> tuple[list[list[str]], float]:
    chosen_subsets = []
    best_seo_measure = -1

    for chosen_variants in itertools.combinations(variants, winners_amount):
        rejected_variants = set(variants) - set(chosen_variants)
        current_seo_measure = seo_measure(
            chosen_variants, rejected_variants, outranking_relation
        )

        if current_seo_measure > best_seo_measure:
            chosen_subsets = [list(chosen_variants)]
            best_seo_measure = current_seo_measure

        elif current_seo_measure == best_seo_measure:
            chosen_subsets.append(list(chosen_variants))

    return chosen_subsets, best_seo_measure
