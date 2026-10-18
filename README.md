# Galileo Mission Analysis Toolkit

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB)
![License](https://img.shields.io/badge/license-MIT-111111)

A small Python toolkit for GNSS mission-analysis concepts inspired by Galileo navigation training. It parses Walker Delta notation, estimates constellation service probability, and builds a simplified Galileo-altitude manoeuvre budget.

> This is a learning project, not an operational Galileo, flight dynamics, or mission operations tool.

Concept notes are in [docs/CONCEPTS.md](docs/CONCEPTS.md). How those notes relate to the navigation programme themes is in [docs/NAVIGATION_PROGRAMME_MAPPING.md](docs/NAVIGATION_PROGRAMME_MAPPING.md).

## What works

| Piece | Module | Behaviour |
|-------|--------|-----------|
| Walker Delta notation | `galileo_mission_analysis.walker` | Parses `i:t/p/f` notation such as `56:24/3/1` and reports satellites per plane, plane separation, in-plane separation, and adjacent-plane phase |
| Availability | `galileo_mission_analysis.availability` | Independent-satellite state probabilities, probability of at least N satellites up, and a month-by-month timeline with linear reliability decay |
| Manoeuvre budget | `galileo_mission_analysis.maneuvers` | Rules-of-thumb delta-v for semi-major axis, inclination, RAAN, relocation, and disposal, plus an ideal-rocket propellant mass |
| Command-line demo | `galileo-mission-analysis` | Prints one fixed reference scenario. Flags: `--walker`, `--months`, `--satellites`, `--required` |
| Example script | `examples/run_reference_scenario.py` | Runs that same demo without installing the package |
| Tests | `tests/` | Seven tests, listed below. They check Walker parsing, availability probabilities, and the manoeuvre rules of thumb |

The signal-in-space and SDR acquisition material is explained in the concept guide only. There is no signal-processing code.

## Install and run

Requires Python 3.10 or newer. The commands below were run on Linux with Python 3.12.3.

```bash
python -m venv .venv
.venv/bin/pip install -e .
.venv/bin/galileo-mission-analysis
```

On Windows the virtualenv executables are `.venv\Scripts\pip` and `.venv\Scripts\galileo-mission-analysis`. That path was not run here.

Run the same demo without installing:

```bash
python examples/run_reference_scenario.py
```

Both commands exited 0 and printed the same text:

```text
Galileo Mission Analysis Portfolio Demo
--------------------------------------
Walker notation: 56:24/3/1
Satellites per plane: 8
Plane separation: 120.0 deg
Adjacent-plane phase: 15.0 deg

Approximate manoeuvre budget
- semi_major_axis_mps: 6.20 m/s
- inclination_mps: 7.68 m/s
- raan_mps: 6.37 m/s
- relocation_mps: 51.26 m/s
- disposal_mps: 12.00 m/s
- total_mps: 83.51 m/s
- propellant for 700 kg dry mass, 220 s Isp: 27.63 kg

Service probability timeline
- month 0: satellite reliability 0.985, P(at least 22 up) 0.995
- month 4: satellite reliability 0.977, P(at least 22 up) 0.983
- month 8: satellite reliability 0.969, P(at least 22 up) 0.963
- month 12: satellite reliability 0.961, P(at least 22 up) 0.935
- month 16: satellite reliability 0.953, P(at least 22 up) 0.899
- month 20: satellite reliability 0.945, P(at least 22 up) 0.857
- month 24: satellite reliability 0.937, P(at least 22 up) 0.810
```

## Tests

Install the test extra and run pytest:

```bash
.venv/bin/pip install -e ".[test]"
.venv/bin/python -m pytest tests -q
```

On Python 3.12.3 and pytest 9.1.1, `pytest tests -q` printed `7 passed in 0.02s`. The verbose run listed these seven tests, all passed:

- `tests/test_availability.py::test_constellation_state_probabilities_sum_to_one`
- `tests/test_availability.py::test_probability_at_least_counts_tail_probability`
- `tests/test_availability.py::test_availability_timeline_declines_with_linear_reliability_decay`
- `tests/test_maneuvers.py::test_galileo_altitude_budget_uses_expected_rules_of_thumb`
- `tests/test_maneuvers.py::test_propellant_mass_is_positive_for_positive_delta_v`
- `tests/test_walker.py::test_parse_walker_delta_notation`
- `tests/test_walker.py::test_invalid_walker_delta_requires_even_plane_split`

`.github/workflows/tests.yml` runs that pytest command and the example script on Python 3.12. The push run for this branch, on Python 3.12.15, printed `7 passed in 0.03s` and then the same scenario text as above.

## Layout

```text
src/galileo_mission_analysis/
  __init__.py
  availability.py
  cli.py
  maneuvers.py
  walker.py
tests/
  conftest.py
  test_availability.py
  test_maneuvers.py
  test_walker.py
examples/run_reference_scenario.py
docs/CONCEPTS.md
docs/NAVIGATION_PROGRAMME_MAPPING.md
```

## Model boundaries

The calculations are the simplified ones in the source, not a flight-dynamics model.

| What the code does | What it leaves out |
|--------------------|--------------------|
| Independent satellite failures | Correlated failures, component reliability, operational history |
| Linear reliability decay down to zero | A reliability model fitted to flight data |
| Probability that at least N satellites are up | User geometry, dilution of precision, orbit propagation, ground segment |
| Galileo-altitude rules of thumb: `\|delta-a\| / 16.13`, `\|delta-i\| * 64`, `\|delta-RAAN\| * 53.1`, relocation phase turned into a semi-major-axis offset | High-fidelity manoeuvre planning |
| Disposal delta-v supplied by the caller | An end-of-life compliance analysis |

## Roadmap

Not implemented:

- Dilution-of-precision geometry
- A synthetic GNSS acquisition demo over code phase and Doppler
- Plots of the availability timeline
- JSON scenario files
- A requirements trace from the docs to functions and tests

## License

MIT. See [LICENSE](LICENSE).
