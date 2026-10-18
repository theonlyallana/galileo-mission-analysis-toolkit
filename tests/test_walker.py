from galileo_mission_analysis.walker import WalkerDelta


def test_parse_walker_delta_notation() -> None:
    walker = WalkerDelta.parse("56:24/3/1")

    assert walker.inclination_deg == 56
    assert walker.total_satellites == 24
    assert walker.planes == 3
    assert walker.satellites_per_plane == 8
    assert walker.plane_separation_deg == 120
    assert walker.in_plane_separation_deg == 45
    assert walker.adjacent_plane_phase_deg == 15
    assert walker.to_notation() == "56:24/3/1"


def test_invalid_walker_delta_requires_even_plane_split() -> None:
    try:
        WalkerDelta.parse("56:25/3/1")
    except ValueError as exc:
        assert "divide evenly" in str(exc)
    else:
        raise AssertionError("Expected invalid Walker notation to fail")

