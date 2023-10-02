from test_data import (
    SEE_PREFERENCES,
    SEE_NAMES,
    RESEARCH_ENTITIES_OUTRANKING_MATRIX,
    RESEARCH_ENTITIES,
)
from timeit import timeit
from enum import Enum
from outranking_relation import OutrankingMatrixNumpy
import ned
from nsga.nsga2_2 import nsga2 as nsga2_2

from nsga.nsga2 import nsga2 as nsga2_1
import seo
import ranked_pairs
import schulz

see_preference_relation = OutrankingMatrixNumpy(
    SEE_PREFERENCES,
    labels=SEE_NAMES,
)

research_entities_outranking_relation = OutrankingMatrixNumpy(
    RESEARCH_ENTITIES_OUTRANKING_MATRIX,
    labels=list(RESEARCH_ENTITIES["id"]),
)


# print(nsga2_2(RESEARCH_ENTITIES["id"], 4, research_entities_outranking_relation))
t2 = timeit(
    lambda: nsga2_2(RESEARCH_ENTITIES["id"], 5, research_entities_outranking_relation),
    number=10,
)

t1 = timeit(
    lambda: nsga2_1(RESEARCH_ENTITIES["id"], 5, research_entities_outranking_relation),
    number=10,
)

print(f"{t1=}, {t2=}")
