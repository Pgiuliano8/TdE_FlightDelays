from dataclasses import dataclass
from model.airport import Airport


@dataclass
class Arco:
    a1: Airport
    a2: Airport
    peso: int