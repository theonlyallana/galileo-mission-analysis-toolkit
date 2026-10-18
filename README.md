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
| Tests | `tests/` | Checks Walker parsing, availability probabilities, and the manoeuvre rules of thumb |

The signal-in-space and SDR acquisition material is explained in the concept guide only. There is no signal-processing code.

## Install and run

Python 3.10 or newer.

```bash
python -m venv .venv
.venv/bin/pip install -e .
.venv/bin/galileo-mission-analysis
```

On Windows, the executables are `.venv\Scripts\pip` and `.venv\Scripts\galileo-mission-analysis`.

Run the same demo without installing:

```bash
python examples/run_reference_scenario.py
```

Install the test extra and run the tests:

```bash
.venv/bin/pip install -e ".[test]"
.venv/bin/python -m pytest tests -q
```

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
