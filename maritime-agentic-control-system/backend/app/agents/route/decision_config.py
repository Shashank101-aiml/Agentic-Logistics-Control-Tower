from dataclasses import dataclass


@dataclass(frozen=True)
class DecisionWeights:
    """
    Multi-objective route decision weights.

    The values represent the relative importance of each
    operational objective. They must sum to 1.0.
    """

    risk: float = 0.40
    cost: float = 0.25
    delay: float = 0.20
    distance: float = 0.15

    def validate(self) -> None:
        total = (
            self.risk
            + self.cost
            + self.delay
            + self.distance
        )

        if abs(total - 1.0) > 1e-6:
            raise ValueError(
                "Decision weights must sum to 1.0. "
                f"Current total: {total}"
            )

        for name, value in {
            "risk": self.risk,
            "cost": self.cost,
            "delay": self.delay,
            "distance": self.distance,
        }.items():
            if value < 0:
                raise ValueError(
                    f"Weight '{name}' cannot be negative."
                )