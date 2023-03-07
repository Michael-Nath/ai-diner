import numpy as np
from typing import List
MINUTES_IN_HOUR = 60

def get_timestring(t: float) -> str:
    hour = str(int(t))
    minute = round((t - int(t)) * MINUTES_IN_HOUR)
    prefix_zero = "0" if minute < 10 else ""
    return f"{hour}:{prefix_zero}{minute} PM"
    
def populate_proportionately(probs: np.ndarray, num_diners: int) -> np.ndarray:
    return probs * num_diners

def dining_times_random(num_diners: int, dining_times_count: int) -> List[int]:
    return np.floor(np.random.rand(num_diners) * dining_times_count)

def reward_short_waits(num_diners: int, received_special: bool) -> float:
    return -(1 / max(0.1, 0.1 * num_diners)) + 10 * received_special