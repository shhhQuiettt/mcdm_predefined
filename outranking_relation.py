from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import numpy as np
import numpy.typing as npt


class OutrankingRelation(ABC):
    no_of_variants: int

    @abstractmethod
    def preference(self, of: Any, over: Any) -> float:
        pass

    @abstractmethod
    def preference_over_indeces(self, of: int, over: int) -> float:
        pass


class OutrankingMatrixNumpy(OutrankingRelation):
    def __init__(self, matrix: npt.ArrayLike, labels: list[Any]) -> None:
        self.matrix = np.array(matrix)
        self.no_of_variants = self.matrix.shape[0]

        self.legend = {label: index for index, label in enumerate(labels)}

    def preference(self, of: Any, over: Any) -> float:
        return self.matrix[self.legend[of], self.legend[over]]

    def preference_over_indeces(self, of: int, over: int) -> float:
        return self.matrix[of, over]
