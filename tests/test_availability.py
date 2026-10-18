from galileo_mission_analysis.availability import (
    Satellite,
    availability_timeline,
    constellation_state_probabilities,
    probability_at_least,
)


def test_constellation_state_probabilities_sum_to_one() -> None:
    satellites = [
        Satellite("SAT-1", 0.98),
        Satellite("SAT-2", 0.97),
        Satellite("SAT-3", 0.96),
    ]

    distribution = constellation_state_probabilities(satellites)

    assert round(sum(distribution.values()), 12) == 1.0
    assert set(distribution) == {0, 1, 2, 3}


def test_probability_at_least_counts_tail_probability() -> None:
    distribution = {0: 0.01, 1: 0.09, 2: 0.3, 3: 0.6}

    assert round(probability_at_least(distribution, 2), 12) == 0.9


def test_availability_timeline_declines_with_linear_reliability_decay() -> None:
    rows = availability_timeline(
        starting_reliability=0.99,
        monthly_decay=0.01,
        months=3,
        satellite_count=4,
        required_available=3,
    )

    assert len(rows) == 4
    assert rows[0]["service_probability"] > rows[-1]["service_probability"]
    assert rows[-1]["satellite_reliability"] == 0.96
