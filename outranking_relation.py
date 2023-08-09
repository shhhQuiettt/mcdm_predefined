from abc import ABC, abstractmethod
from typing import Any, Dict
import numpy as np
import numpy.typing as npt


class OutrankingRelation(ABC):
    @abstractmethod
    def preference(self, of: Any, over: Any) -> float:
        pass


class OutrankingMatrixNumpy(OutrankingRelation):
    def __init__(self, matrix: npt.ArrayLike, labels: list[str]) -> None:
        self.matrix = np.array(matrix)
        self.legend = {label: index for index, label in enumerate(labels)}

    def preference(self, of: Any, over: Any) -> float:
        return self.matrix[self.legend[of], self.legend[over]]
