from test_data import (
    RESEARCH_ENTITIES_OUTRANKING_MATRIX,
    RESEARCH_ENTITIES,
)
from outranking_relation import OutrankingMatrixNumpy
from nsga2 import ChoosingVariants


research_entities_preference_relation = OutrankingMatrixNumpy(
    RESEARCH_ENTITIES_OUTRANKING_MATRIX, labels=RESEARCH_ENTITIES["id"]
)

alg = ChoosingVariants(
    chosen_amount=5,
    outranking_relation=research_entities_preference_relation,
)

out = dict()

# chosen = [11, 402, 451, 485, 504]
chosen = [11, 402, 485, 504, 910]
chosen_ids = [1 if el in chosen else 0 for el in RESEARCH_ENTITIES["id"]]

alg._evaluate(chosen_ids, out)
print(out)
