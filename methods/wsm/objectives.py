from outranking_relation import OutrankingRelation


def chosen_strength(chosen_subset: list, outranking_relation, variants: list) -> float:
    strength = 0
    for chosen_variant in chosen_subset:
        for rejected_variant in (v for v in variants if v not in chosen_subset):
            strength += outranking_relation.preference(
                of=chosen_variant, over=rejected_variant
            )

    return strength


def rejected_weakness(
    subset: list, outranking_relation: OutrankingRelation, variants: list
) -> float:
    weakness = 0

    for rejected_variant in (v for v in variants if v not in subset):
        weakness += max(
            (
                outranking_relation.preference(of=chosen_variant, over=rejected_variant)
                for chosen_variant in subset
            )
        )

    return weakness


def rejected_strength(
    chosen_subset: list, outranking_relation, variants: list
) -> float:
    strength = 0

    for rejected_variant in (v for v in variants if v not in chosen_subset):
        for chosen_variant in chosen_subset:
            strength += outranking_relation.preference(
                of=rejected_variant, over=chosen_variant
            )

    return strength


def chosen_weakness(chosen_subset: list, outranking_relation, variants: list) -> float:
    max_preferences_rejected_over_chosen = []

    for rejected_variant in (v for v in variants if v not in chosen_subset):
        max_preferences_rejected_over_chosen.append(
            max(
                (
                    outranking_relation.preference(
                        of=rejected_variant, over=chosen_variant
                    )
                )
                for chosen_variant in chosen_subset
            )
        )

    return min(max_preferences_rejected_over_chosen)
