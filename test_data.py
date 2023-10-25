import pandas as pd
from outranking_relation.electre3 import (
    Criterion,
    CriterionType,
    get_outranking_relation,
)

SEE_NAMES = ["KAM", "KOS", "KRA", "LEG", "LOD", "MIE", "POM", "SLU", "STA", "TAR"]
SEE_PREFERENCES = [
    [0.000, 0.330, 0.330, 0.330, 0.330, 0.330, 0.330, 0.197, 0.027, 0.330],
    [0.670, 0.000, 0.359, 0.670, 0.574, 0.574, 0.797, 0.670, 0.670, 0.690],
    [0.670, 0.374, 0.000, 0.695, 0.330, 0.330, 0.625, 0.670, 0.670, 0.530],
    [0.670, 0.330, 0.305, 0.000, 0.634, 0.634, 0.634, 0.527, 0.670, 0.330],
    [0.670, 0.225, 0.592, 0.366, 0.000, 0.305, 0.730, 0.670, 0.670, 0.305],
    [0.670, 0.265, 0.670, 0.366, 0.435, 0.000, 1.000, 0.670, 0.670, 0.383],
    [0.670, 0.000, 0.171, 0.366, 0.270, 0.000, 0.000, 0.670, 0.670, 0.144],
    [0.729, 0.330, 0.270, 0.330, 0.330, 0.330, 0.330, 0.000, 0.197, 0.330],
    [0.562, 0.330, 0.326, 0.330, 0.330, 0.330, 0.330, 0.131, 0.000, 0.330],
    [0.670, 0.170, 0.316, 0.670, 0.574, 0.530, 0.800, 0.670, 0.670, 0.000],
]

RESEARCH_ENTITIES = pd.DataFrame(
    columns=[
        "id",
        "Publications",
        "Potential",
        "Commercialization",
        "Other achievements",
    ],
    data=[
        [2, 45.93, 2, 0, 17],
        [4, 64.37, 973.93, 2.02, 92],
        [11, 94.11, 1121, 5.06, 92],
        [36, 51.88, 235.2, 0.68, 35],
        [389, 62.12, 210.06, 1.23, 46],
        [390, 70.25, 194.05, 0.81, 58],
        [395, 90.54, 242.61, 0.68, 63],
        [402, 89.75, 1165.43, 4.34, 83],
        [403, 63.08, 480.46, 6.11, 58],
        [410, 57.82, 132.9, 0.19, 35],
        [418, 52.22, 100.72, 0.89, 42],
        [424, 75.75, 302.5, 2.48, 65],
        [433, 61.54, 861.18, 2.07, 85],
        [442, 57.45, 498.39, 1.62, 43],
        [448, 79.03, 269.77, 7.48, 80],
        [449, 58.15, 508.26, 1.2, 69],
        [451, 88.82, 525.47, 5.24, 82],
        [458, 53.72, 284.18, 0.86, 50],
        [463, 70.27, 1282.04, 2.12, 71],
        [466, 60.86, 323, 2.92, 75],
        [476, 53.66, 203.09, 0.45, 38],
        [485, 77.09, 1408, 5.69, 90],
        [486, 63.76, 524.51, 3.02, 41],
        [503, 80.18, 1141.07, 2.68, 92],
        [504, 112.37, 330.9, 4.76, 88],
        [505, 61.11, 395.57, 3.72, 80],
        [515, 64.93, 473.1, 10.15, 69],
        [529, 60.29, 11, 0, 0],
        [825, 62.5, 108.56, 4.68, 40],
        [897, 65.65, 345.43, 2.34, 76],
        [904, 27.58, 14, 4.17, 33],
        [910, 77.24, 678, 13.32, 48],
        [912, 48.59, 492.97, 4.34, 31],
        [926, 48, 0, 0, 22],
        [958, 70.13, 32.43, 4.45, 42],
        [960, 63.16, 20, 0, 37],
        [975, 0, 0.2, 0, 17],
        [987, 60.85, 367.16, 1.47, 71],
        [988, 55.66, 274.4, 0.38, 65],
    ],
)

RESEARCH_ENTITIES_NAMES = list(RESEARCH_ENTITIES["id"])

RESEARCH_ENTITIES_CRITERIA = [
    Criterion(
        name="Publications",
        criterion_type=CriterionType.GAIN,
        weight=0.65,
        indifference_threshold=5,
        preference_threshold=15,
        veto_threshold=30,
    ),
    Criterion(
        name="Potential",
        criterion_type=CriterionType.GAIN,
        weight=0.1,
        indifference_threshold=20,
        preference_threshold=50,
    ),
    Criterion(
        name="Commercialization",
        criterion_type=CriterionType.GAIN,
        weight=0.15,
        indifference_threshold=0.5,
        preference_threshold=1.2,
    ),
    Criterion(
        name="Other achievements",
        criterion_type=CriterionType.GAIN,
        weight=0.1,
        indifference_threshold=4,
        preference_threshold=12,
    ),
]

RESEARCH_ENTITIES_OUTRANKING_MATRIX = get_outranking_relation(
    RESEARCH_ENTITIES, RESEARCH_ENTITIES_CRITERIA
)
