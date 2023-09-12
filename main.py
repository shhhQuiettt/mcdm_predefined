from test_data import (
    SEE_PREFERENCES,
    SEE_NAMES,
    # RESEARCH_ENTITIES_OUTRANKING_MATRIX,
    # RESEARCH_ENTITIES,
)
from enum import Enum
from outranking_relation import OutrankingMatrixNumpy
import ned
import nsga2
import seo
import ranked_pairs
import schulz

see_preference_relation = OutrankingMatrixNumpy(
    SEE_PREFERENCES,
    labels=SEE_NAMES,
)


print(schulz.schulz(SEE_NAMES, 4, see_preference_relation))
