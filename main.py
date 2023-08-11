from test_data import SEE_PREFERENCES, SEE_NAMES, RESEARCH_ENTITIES_OUTRANKING_MATRIX
from enum import Enum
from outranking_relation import OutrankingMatrixNumpy
import ned
import seo
import ranked_pairs

# see_preference_relation = OutrankingMatrixNumpy(
#     SEE_PREFERENCES,
#     labels=SEE_NAMES,
# )

# print(ned.ned(SEE_NAMES, 4, see_preference_relation))
# print(ranked_pairs.ranked_pairs(SEE_NAMES, 4, see_preference_relation))
print(RESEARCH_ENTITIES_OUTRANKING_MATRIX)
