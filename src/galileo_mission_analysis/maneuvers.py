"""Approximate manoeuvre budget utilities for Galileo-altitude scenarios."""

from __future__ import annotations

from dataclasses import dataclass
from math import exp

G0 = 9.80665


@dataclass(frozen=True)
class DeltaVBudget:
    """Breakdown of simplified manoeuvre delta-v terms."""

    semi_major_axis_mps: float
    inclination_mps: float
    raan_mps: float
    relocation_mps: float
    disposal_mps: float

    @property
    def total_mps(self) -> float:
        return (
            self.semi_major_axis_mps
            + self.inclination_mps
            + self.raan_mps
            + self.relocation_mps
            + self.disposal_mps
        )

    def propellant_mass_kg(self, dry_mass_kg: float, isp_seconds: float) -> float:
        """Estimate propellant mass using the ideal rocket equation."""

        if dry_mass_kg <= 0.0:
            raise ValueError("dry_mass_kg must be positive")
        if isp_seconds <= 0.0:
            raise ValueError("isp_seconds must be positive")

        mass_ratio = exp(self.total_mps / (isp_seconds * G0))
        return dry_mass_kg * (mass_ratio - 1.0)

    def as_dict(self) -> dict[str, float]:
        return {
            "semi_major_axis_mps": self.semi_major_axis_mps,
            "inclination_mps": self.inclination_mps,
            "raan_mps": self.raan_mps,
            "relocation_mps": self.relocation_mps,
            "disposal_mps": self.disposal_mps,
            "total_mps": self.total_mps,
        }


def galileo_altitude_budget(
    delta_a_km: float = 0.0,
    delta_inclination_deg: float = 0.0,
    delta_raan_deg: float = 0.0,
    relocation_phase_deg: float = 0.0,
    relocation_days: float = 1.0,
    disposal_mps: float = 0.0,
) -> DeltaVBudget:
    """Estimate delta-v terms using simple Galileo-altitude rules of thumb.

    The constants are portfolio approximations inspired by training exercises:
    |delta-a| / 16.13, |delta-i| * 64, and |delta-RAAN| * 53.1. Relocation is
    modelled by converting required phase drift into a semi-major-axis offset.
    """

    if relocation_days <= 0.0:
        raise ValueError("relocation_days must be positive")
    if disposal_mps < 0.0:
        raise ValueError("disposal_mps must be non-negative")

    semi_major_axis_mps = abs(delta_a_km) / 16.13
    inclination_mps = abs(delta_inclination_deg) * 64.0
    raan_mps = abs(delta_raan_deg) * 53.1

    drift_delta_a_km = abs(relocation_phase_deg) * 32.154 / relocation_days
    relocation_mps = drift_delta_a_km / 16.13

    return DeltaVBudget(
        semi_major_axis_mps=semi_major_axis_mps,
        inclination_mps=inclination_mps,
        raan_mps=raan_mps,
        relocation_mps=relocation_mps,
        disposal_mps=disposal_mps,
    )

