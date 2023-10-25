from methods.nsga.nsga2_binary import nsga2 as nsga2_binary
from methods.nsga.nsga2_discrete import nsga2 as nsga2_discrete
from methods.ned import ned
from methods.seo import seo
from methods.schulz import schulz

from outranking_relation.outranking_relation import OutrankingMatrixNumpy
from test_data import (
    RESEARCH_ENTITIES_NAMES,
    RESEARCH_ENTITIES_OUTRANKING_MATRIX,
    SEE_NAMES,
    SEE_OUTRANKING_MATRIX,
)

outranking_relation_RE = OutrankingMatrixNumpy(
    RESEARCH_ENTITIES_OUTRANKING_MATRIX,
    RESEARCH_ENTITIES_NAMES,
)

outanking_relation_SEE = OutrankingMatrixNumpy(
    SEE_OUTRANKING_MATRIX,
    SEE_NAMES,
)

nsga_res_bin = nsga2_binary(
    RESEARCH_ENTITIES_NAMES, chosen_amount=5, outranking_relation=outranking_relation_RE
)

print(f"NSGA binary {nsga_res_bin}")
nsga_res_dis = nsga2_discrete(
    RESEARCH_ENTITIES_NAMES, chosen_amount=5, outranking_relation=outranking_relation_RE
)
print(f"NSGA discrete {nsga_res_dis}")

print()
print("SEE")
ned_res = ned(SEE_NAMES, chosen_amount=5, outranking_relation=outanking_relation_SEE)
print(f"NED {ned_res}")

seo_res = seo(SEE_NAMES, chosen_amount=5, outranking_relation=outanking_relation_SEE)
print(f"SEO {seo_res}")

schulz_res = schulz(
    SEE_NAMES, chosen_amount=5, outranking_relation=outanking_relation_SEE
)
print(f"Schulz {schulz_res}")
