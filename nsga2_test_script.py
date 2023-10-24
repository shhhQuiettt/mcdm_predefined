from test_data import (
    RESEARCH_ENTITIES_OUTRANKING_MATRIX,
    RESEARCH_ENTITIES,
)
from outranking_relation import OutrankingMatrixNumpy

from nsga.nsga2 import ChoosingVariants

# from convex import objective_functions

# from nsga.nsga2_2 import ChoosingVariants


research_entities_preference_relation = OutrankingMatrixNumpy(
    RESEARCH_ENTITIES_OUTRANKING_MATRIX, labels=RESEARCH_ENTITIES["id"]
)

alg = ChoosingVariants(
    chosen_amount=5,
    outranking_relation=research_entities_preference_relation,
)

out = dict()

# chosen = [11, 402, 451, 485, 504]
chosen = [11, 395, 402, 451, 504]
chosen_ids = [1 if el in chosen else 0 for el in RESEARCH_ENTITIES["id"]]
# chosen_uds = [list(RESEARCH_ENTITIES["id"]).index(el) for el in chosen]

# print(
#     [
#         f(chosen, research_entities_preference_relation, list(RESEARCH_ENTITIES["id"]))
#         for f in objective_functions
#     ]
# )

print(chosen_ids)
alg._evaluate(chosen_ids, out)
print(out)
