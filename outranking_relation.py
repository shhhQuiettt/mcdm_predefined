from abc import ABC, abstractmethod
from typing import Any, Dict
import numpy as np
import numpy.typing as npt


class OutrankingMatrix(ABC):
    @abstractmethod
    def preference(of: Any, over: Any) -> float:
        pass


class OutrankingMatrixNumpy(OutrankingMatrix):
    def __init__(self, matrix: npt.ArrayLike, legend: Dict[Any, int]) -> None:
        self.matrix = np.array(matrix)
        self.legend = legend

    def preference(self, of: Any, over: Any) -> float:
        return self.matrix[self.legend[of], self.legend[over]]
