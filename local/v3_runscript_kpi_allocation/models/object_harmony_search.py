from pydantic import BaseModel
from typing import Any, Optional
from torch import Tensor
from services.truncated_normal_service import TruncatedNormalService


class ObjectHarmonySearch(BaseModel):
    lower_bound: Optional[float]
    upper_bound: Optional[float]
    max_improvisations: int
    hms: int
    hmcr: float
    par: float
    bw: float
    lower_upper_matrix: Any

    def __init__(self, lower_upper_matrix: Any, max_improvisations: int, hms: int, hmcr: float = 0.75, par: float = 0.5, bw: float = 0.5, lower_bound: float = None, upper_bound: float = None):
        hmcr = 0.75
        par = 0.5
        bw = 0.5

        super().__init__(max_improvisations=max_improvisations, hms=hms, hmcr=hmcr, par=par, bw=bw,
                         lower_bound=lower_bound, upper_bound=upper_bound, lower_upper_matrix=lower_upper_matrix)

    def get_fitness(self, harmony: Tensor) -> float:
        penalty = 0
        task_weight = harmony.sum(dim=0)
        if (task_weight < 1).any():
            penalty += float('+inf')

        fitness = task_weight.sum() + penalty

        return fitness.item()

    def get_fitness_base_kpi(self, vector: Tensor) -> float:
        # print(vector)
        task_weight = vector.sum(dim=1)
        penalty = 0
        if (task_weight < 1).any():
            penalty += float('+inf')

        fitness = task_weight.sum() + penalty
        return fitness

    def get_value(self) -> float:
        t_normal = TruncatedNormalService(
            min_val=self.lower_bound, max_val=self.upper_bound)
        size = (6)
        return t_normal.generate_truncated_normal_with_sum(size=size)

    def set_lower_bound(self, lower_bound: float) -> None:
        self.lower_bound = lower_bound

    def set_upper_bound(self, upper_bound: float) -> None:
        self.upper_bound = upper_bound
