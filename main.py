from test_data import (
    SEE_PREFERENCES,
    SEE_NAMES,
    RESEARCH_ENTITIES_OUTRANKING_MATRIX,
    RESEARCH_ENTITIES,
)
from enum import Enum
from outranking_relation import OutrankingMatrixNumpy
import ned
import nsga2
import seo
import ranked_pairs

# see_preference_relation = OutrankingMatrixNumpy(
#     SEE_PREFERENCES,
#     labels=SEE_NAMES,
# )

# print(ned.ned(SEE_NAMES, 4, see_preference_relation))
# print(ranked_pairs.ranked_pairs(SEE_NAMES, 4, see_preference_relation))
# print(RESEARCH_ENTITIES_OUTRANKING_MATRIX)

research_entities_preference_relation = OutrankingMatrixNumpy(
    RESEARCH_ENTITIES_OUTRANKING_MATRIX, labels=RESEARCH_ENTITIES["id"]
)

nsga2.nsga2(
    RESEARCH_ENTITIES["id"],
    chosen_amount=5,
    outranking_relation=research_entities_preference_relation,
)
