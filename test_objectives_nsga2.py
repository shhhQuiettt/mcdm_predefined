from methods.nsga.nsga2_discrete import ChoosingVariants as ChoosingVariantsDiscrete
from methods.nsga.nsga2_binary import ChoosingVariants as ChoosingVariantsBinary

from test_data import RESEARCH_ENTITIES_NAMES, RESEARCH_ENTITIES_OUTRANKING_MATRIX
from outranking_relation.outranking_relation import OutrankingMatrixNumpy

outranking_relation = OutrankingMatrixNumpy(
    RESEARCH_ENTITIES_OUTRANKING_MATRIX,
    RESEARCH_ENTITIES_NAMES,
)
subset = [11, 402, 451, 485, 504]
subset_ids = [i for i, name in enumerate(RESEARCH_ENTITIES_NAMES) if name in subset]

subset_binary_flags = [
    1 if i in subset_ids else 0 for i in range(len(RESEARCH_ENTITIES_NAMES))
]

out_d = dict()

ChoosingVariantsDiscrete(outranking_relation, 5)._evaluate(subset_ids, out=out_d)
print(out_d)

out_b = dict()
ChoosingVariantsBinary(outranking_relation, 5)._evaluate(subset_binary_flags, out=out_b)
print(out_b)
