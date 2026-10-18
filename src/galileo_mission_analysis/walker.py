"""Walker Delta constellation notation helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WalkerDelta:
    """Represent Walker Delta notation as i:t/p/f."""

    inclination_deg: float
    total_satellites: int
    planes: int
    relative_spacing: int

    def __post_init__(self) -> None:
        if self.total_satellites <= 0:
            raise ValueError("total_satellites must be positive")
        if self.planes <= 0:
            raise ValueError("planes must be positive")
        if self.total_satellites % self.planes != 0:
            raise ValueError("total_satellites must divide evenly across planes")
        if self.relative_spacing < 0:
            raise ValueError("relative_spacing must be non-negative")

    @classmethod
    def parse(cls, notation: str) -> "WalkerDelta":
        """Parse notation such as '56:24/3/1'."""

        try:
            inclination_text, rest = notation.split(":")
            total_text, planes_text, spacing_text = rest.split("/")
        except ValueError as exc:
            raise ValueError("Walker notation must look like '56:24/3/1'") from exc

        return cls(
            inclination_deg=float(inclination_text),
            total_satellites=int(total_text),
            planes=int(planes_text),
            relative_spacing=int(spacing_text),
        )

    @property
    def satellites_per_plane(self) -> int:
        return self.total_satellites // self.planes

    @property
    def plane_separation_deg(self) -> float:
        return 360.0 / self.planes

    @property
    def in_plane_separation_deg(self) -> float:
        return 360.0 / self.satellites_per_plane

    @property
    def adjacent_plane_phase_deg(self) -> float:
        return self.relative_spacing * 360.0 / self.total_satellites

    def to_notation(self) -> str:
        inclination = f"{self.inclination_deg:g}"
        return f"{inclination}:{self.total_satellites}/{self.planes}/{self.relative_spacing}"

    def summary(self) -> dict[str, float]:
        return {
            "inclination_deg": self.inclination_deg,
            "total_satellites": float(self.total_satellites),
            "planes": float(self.planes),
            "satellites_per_plane": float(self.satellites_per_plane),
            "plane_separation_deg": self.plane_separation_deg,
            "in_plane_separation_deg": self.in_plane_separation_deg,
            "adjacent_plane_phase_deg": self.adjacent_plane_phase_deg,
        }

