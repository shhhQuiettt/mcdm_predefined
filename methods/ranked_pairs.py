from collections.abc import Iterable
from outranking_relation import OutrankingRelation
import itertools


def get_preference_pair(
    variant1: str, variant2: str, outranking_relation: OutrankingRelation
) -> tuple[str, str]:
    if outranking_relation.preference(
        variant1, variant2
    ) > outranking_relation.preference(variant2, variant1):
        return (variant1, variant2)
    else:
        return (variant2, variant1)


def adding_arc_generates_cycle(
    arc_to_add: tuple[str, str], arcs: Iterable[tuple[str, str]]
) -> bool:
    def check_if_path_exists(
        start: str, end: str, arcs: Iterable[tuple[str, str]]
    ) -> bool:
        if start == end:
            return True

        for arc in arcs:
            if arc[0] == start:
                return check_if_path_exists(arc[1], end, arcs)
        return False

    return check_if_path_exists(arc_to_add[1], arc_to_add[0], arcs)


def ranked_pairs(
    variants: list[str], winners_amount: int, outranking_relation: OutrankingRelation
) -> list[str]:
    preference_pairs = {}
    for variant1, variant2 in itertools.combinations(variants, 2):
        winner, loser = get_preference_pair(variant1, variant2, outranking_relation)

        preference_difference = outranking_relation.preference(
            winner, loser
        ) - outranking_relation.preference(loser, winner)

        if not adding_arc_generates_cycle((winner, loser), preference_pairs.keys()):
            preference_pairs[(winner, loser)] = (
                preference_difference,
                outranking_relation.preference(winner, loser),
            )

    sorted_preference_pairs = sorted(
        preference_pairs.keys(), key=lambda k: preference_pairs[k], reverse=True
    )

    return sorted_preference_pairs[:winners_amount]
