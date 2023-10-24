from .objectives import (
    chosen_strength,
    rejected_weakness,
    rejected_strength,
    chosen_weakness,
)
from outranking_relation import OutrankingMatrixNumpy
from functools import partial


from test_data import (
    RESEARCH_ENTITIES_OUTRANKING_MATRIX,
    RESEARCH_ENTITIES,
)

outranking_relation = OutrankingMatrixNumpy(
    RESEARCH_ENTITIES_OUTRANKING_MATRIX,
    labels=list(RESEARCH_ENTITIES["id"]),
)

objective_functions = [
    partial(
        chosen_strength,
        variants=list(RESEARCH_ENTITIES["id"]),
        outranking_relation=outranking_relation,
    ),
    partial(
        rejected_weakness,
        variants=list(RESEARCH_ENTITIES["id"]),
        outranking_relation=outranking_relation,
    ),
    partial(
        rejected_strength,
        variants=list(RESEARCH_ENTITIES["id"]),
        outranking_relation=outranking_relation,
    ),
    partial(
        chosen_weakness,
        variants=list(RESEARCH_ENTITIES["id"]),
        outranking_relation=outranking_relation,
    ),
]


def run():
    print([f([11, 395, 402, 451, 504]) for f in objective_functions])
