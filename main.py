from test_data import RESEARCH_ENTITIES_NAMES, RESEARCH_ENTITIES_OUTRANKING_MATRIX
import numpy as np
import matplotlib.pyplot as plt

print(RESEARCH_ENTITIES_OUTRANKING_MATRIX)

# heatmap
fig, ax = plt.subplots()
im = ax.imshow(RESEARCH_ENTITIES_OUTRANKING_MATRIX, cmap="hot", interpolation="nearest")
im.set_clim(-1, 1)
ax.set_xticks(np.arange(len(RESEARCH_ENTITIES_NAMES)))
ax.set_yticks(np.arange(len(RESEARCH_ENTITIES_NAMES)))
ax.set_xticklabels(RESEARCH_ENTITIES_NAMES)
ax.set_yticklabels(RESEARCH_ENTITIES_NAMES)
plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
plt.show()
