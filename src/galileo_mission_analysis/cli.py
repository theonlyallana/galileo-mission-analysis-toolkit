"""Command-line demo for the Galileo mission-analysis toolkit."""

from __future__ import annotations

import argparse

from .availability import availability_timeline
from .maneuvers import galileo_altitude_budget
from .walker import WalkerDelta


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a simplified GNSS mission-analysis scenario.")
    parser.add_argument("--walker", default="56:24/3/1", help="Walker Delta notation, e.g. 56:24/3/1")
    parser.add_argument("--months", type=int, default=24, help="Months to simulate")
    parser.add_argument("--satellites", type=int, default=24, help="Number of satellites in the availability model")
    parser.add_argument("--required", type=int, default=22, help="Minimum satellites required for service")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    walker = WalkerDelta.parse(args.walker)
    budget = galileo_altitude_budget(
        delta_a_km=-100.0,
        delta_inclination_deg=0.12,
        delta_raan_deg=0.12,
        relocation_phase_deg=180.0,
        relocation_days=7.0,
        disposal_mps=12.0,
    )
    timeline = availability_timeline(
        starting_reliability=0.985,
        monthly_decay=0.002,
        months=args.months,
        satellite_count=args.satellites,
        required_available=args.required,
    )

    print("Galileo Mission Analysis Portfolio Demo")
    print("--------------------------------------")
    print(f"Walker notation: {walker.to_notation()}")
    print(f"Satellites per plane: {walker.satellites_per_plane}")
    print(f"Plane separation: {walker.plane_separation_deg:.1f} deg")
    print(f"Adjacent-plane phase: {walker.adjacent_plane_phase_deg:.1f} deg")
    print()
    print("Approximate manoeuvre budget")
    for label, value in budget.as_dict().items():
        print(f"- {label}: {value:.2f} m/s")
    print(f"- propellant for 700 kg dry mass, 220 s Isp: {budget.propellant_mass_kg(700, 220):.2f} kg")
    print()
    print("Service probability timeline")
    for row in timeline[:: max(1, len(timeline) // 6)]:
        print(
            f"- month {row['month']:.0f}: "
            f"satellite reliability {row['satellite_reliability']:.3f}, "
            f"P(at least {args.required} up) {row['service_probability']:.3f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

