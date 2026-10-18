from galileo_mission_analysis.maneuvers import galileo_altitude_budget


def test_galileo_altitude_budget_uses_expected_rules_of_thumb() -> None:
    budget = galileo_altitude_budget(
        delta_a_km=-100,
        delta_inclination_deg=0.12,
        delta_raan_deg=0.12,
        relocation_phase_deg=180,
        relocation_days=7,
        disposal_mps=12,
    )

    assert round(budget.semi_major_axis_mps, 2) == 6.20
    assert round(budget.inclination_mps, 2) == 7.68
    assert round(budget.raan_mps, 2) == 6.37
    assert budget.total_mps > 80


def test_propellant_mass_is_positive_for_positive_delta_v() -> None:
    budget = galileo_altitude_budget(delta_a_km=100, disposal_mps=10)

    assert budget.propellant_mass_kg(dry_mass_kg=700, isp_seconds=220) > 0

