from outranking_relation import OutrankingRelation
import itertools
from typing import Iterable


def ned_measure(
    chosen_variants: Iterable[str],
    rejected_variants: Iterable[str],
    outranking_relation: OutrankingRelation,
) -> int:
    return sum(
        1
        for chosen, rejected in itertools.product(chosen_variants, rejected_variants)
        if outranking_relation.preference(chosen, rejected)
        > outranking_relation.preference(rejected, chosen)
    )


def ned(
    variants: list[str], winners_amount: int, outranking_relation: OutrankingRelation
) -> tuple[list[list[str]], int]:
    chosen_subsets = []
    best_ned_measure = -1

    for chosen_variants in itertools.combinations(variants, winners_amount):
        rejected_variants = set(variants) - set(chosen_variants)
        current_ned_measure = ned_measure(
            chosen_variants, rejected_variants, outranking_relation
        )

        if current_ned_measure > best_ned_measure:
            chosen_subsets = [list(chosen_variants)]
            best_ned_measure = current_ned_measure

        elif current_ned_measure == best_ned_measure:
            chosen_subsets.append(list(chosen_variants))

    return chosen_subsets, best_ned_measure
