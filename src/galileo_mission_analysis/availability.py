"""Simplified constellation availability calculations.

The functions in this module are intentionally small and auditable. They model
independent satellite availability states, which is useful for learning and
portfolio demonstration, not operational Galileo analysis.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import comb


@dataclass(frozen=True)
class Satellite:
    """A satellite with an independent probability of being serviceable."""

    name: str
    reliability: float
    service_availability: float = 1.0

    def __post_init__(self) -> None:
        for label, value in (
            ("reliability", self.reliability),
            ("service_availability", self.service_availability),
        ):
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{label} must be between 0 and 1")

    @property
    def up_probability(self) -> float:
        """Probability the satellite is both healthy and available for service."""

        return self.reliability * self.service_availability


def binomial_state_probabilities(satellite_count: int, up_probability: float) -> dict[int, float]:
    """Return P(k satellites available) for identical independent satellites."""

    if satellite_count < 0:
        raise ValueError("satellite_count must be non-negative")
    if not 0.0 <= up_probability <= 1.0:
        raise ValueError("up_probability must be between 0 and 1")

    return {
        k: comb(satellite_count, k)
        * (up_probability**k)
        * ((1.0 - up_probability) ** (satellite_count - k))
        for k in range(satellite_count + 1)
    }


def constellation_state_probabilities(satellites: list[Satellite]) -> dict[int, float]:
    """Return P(k satellites available) for non-identical independent satellites."""

    distribution = {0: 1.0}
    for satellite in satellites:
        p_up = satellite.up_probability
        next_distribution: dict[int, float] = {}
        for available_count, probability in distribution.items():
            next_distribution[available_count] = (
                next_distribution.get(available_count, 0.0) + probability * (1.0 - p_up)
            )
            next_distribution[available_count + 1] = (
                next_distribution.get(available_count + 1, 0.0) + probability * p_up
            )
        distribution = next_distribution
    return distribution


def probability_at_least(distribution: dict[int, float], required_available: int) -> float:
    """Return the probability of at least N available satellites."""

    return sum(probability for count, probability in distribution.items() if count >= required_available)


def availability_timeline(
    starting_reliability: float,
    monthly_decay: float,
    months: int,
    satellite_count: int,
    required_available: int,
) -> list[dict[str, float]]:
    """Estimate service availability over time for identical satellites.

    Reliability decays linearly here to keep the model transparent. A real
    mission analysis would use a reliability model fitted to component and
    in-flight performance data.
    """

    if months < 0:
        raise ValueError("months must be non-negative")
    if monthly_decay < 0.0:
        raise ValueError("monthly_decay must be non-negative")

    rows: list[dict[str, float]] = []
    for month in range(months + 1):
        reliability = max(0.0, starting_reliability - monthly_decay * month)
        distribution = binomial_state_probabilities(satellite_count, reliability)
        rows.append(
            {
                "month": float(month),
                "satellite_reliability": reliability,
                "service_probability": probability_at_least(distribution, required_available),
            }
        )
    return rows

