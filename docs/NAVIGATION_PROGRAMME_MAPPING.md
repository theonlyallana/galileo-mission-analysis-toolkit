# Navigation Programme Mapping

This file maps the project back to the navigation programme material that inspired it. It is written as an original summary rather than copied course content.

## Source Topics Incorporated

| Navigation programme topic | How this project incorporates it |
|----------------------------|----------------------------------|
| Galileo constellation and mission analysis | Walker Delta parsing, constellation geometry summaries, and simplified mission-analysis scenario |
| Service availability computation | Probability that at least a required number of satellites are available |
| Satellite reliability | Per-satellite reliability inputs and reliability decay timeline |
| Walker constellation parameters | `WalkerDelta` class parses notation and computes spacing relationships |
| Delta-v budgeting | Simplified correction, relocation, and disposal budget utilities |
| Injection/orbit correction ideas | Semi-major-axis, inclination, and RAAN correction terms |
| Station-keeping and relocation | Relocation phasing estimate and manoeuvre budget structure |
| Disposal planning | Disposal delta-v included in total budget |
| Galileo signal architecture and SIS processing | Explained in docs and marked as a future SDR/acquisition module |
| SDR / I/Q / GNURadio acquisition workflow | Roadmap item for a future synthetic acquisition explainer |
| Requirements engineering | Project scope, assumptions, tests, and caveats define what the tool must and must not do |
| Capella / ARCADIA / MBSE | Reflected in traceable documentation: concept, implementation, caveat, verification |
| ECSS-style engineering discipline | Clear model boundaries, verification evidence, and no overclaiming |

## What Was Intentionally Not Copied

This repo does not include:

- ESA slides
- course workbook data
- proprietary operational parameters
- raw screenshots
- copied diagrams
- claims that the model is validated for flight or Galileo operations

Instead, it turns the learning themes into original software and original documentation.

## Project Feature Traceability

| Repo feature | Source learning theme | Evidence in repo |
|--------------|----------------------|------------------|
| `WalkerDelta` | Walker constellation notation and orbital plane spacing | `src/galileo_mission_analysis/walker.py` |
| `availability_timeline` | Service availability and reliability evolution | `src/galileo_mission_analysis/availability.py` |
| `constellation_state_probabilities` | Probability of constellation states | `src/galileo_mission_analysis/availability.py` |
| `galileo_altitude_budget` | Delta-v budget approximations for correction, relocation, disposal | `src/galileo_mission_analysis/maneuvers.py` |
| CLI reference scenario | Integrated mission-analysis demonstration | `src/galileo_mission_analysis/cli.py` |
| Tests | Verification mindset | `tests/` |
| Concept guide | Communication and systems thinking | `docs/CONCEPTS.md` |

## Recruiter-Friendly Story

This project lets Andrew say:

> I took Galileo navigation programme material and converted the core mission-analysis ideas into a small tested Python toolkit. It covers Walker constellation notation, constellation availability, simplified manoeuvre budgeting, and clear model limitations. It is not an operational model, but it shows I can translate navigation training into executable engineering work.

## Interview Talking Points

### GMV / GNSS Algorithms

- The project is a bridge from Galileo programme exposure into algorithmic thinking.
- It shows comfort with GNSS constellation terminology and probability models.
- It gives a concrete artifact to discuss before deeper topics such as WLS, Kalman filtering, PPP, and RTK.

### ESA / Systems Engineering

- The repo is deliberately scoped and caveated.
- Documentation maps source learning to implementation and verification.
- Tests serve as a small-scale validation layer.

### SSTL / Mission Analysis

- Walker notation and delta-v budgets are directly relevant to mission-analysis literacy.
- The project shows the habit of turning mission concepts into tools.

### Starlink / SpaceX-Adjacent Positioning

- Constellation availability, phasing, service continuity, and operations budgets are all relevant to large satellite networks.
- The project is simple, but the thinking pattern scales: define the service, model the constellation state, quantify constraints, and verify assumptions.

## Next Content To Add

The strongest next expansions would be:

1. A simple Dilution of Precision style geometry module.
2. A synthetic GNSS acquisition demo using correlation over code phase and Doppler bins.
3. A visual service-availability plot over time.
4. A small JSON scenario format so users can define their own constellation case.
5. A Capella-inspired requirements trace table connecting requirements to tests.

