# DAWN

## Resilient Autonomous UAV Engineering Project

DAWN is a personal aerospace engineering project focused on the progressive
development, simulation, integration, and validation of a resilient autonomous
unmanned aerial vehicle.

The project is intended to integrate flight dynamics, Guidance, Navigation and
Control (GNC), state estimation, autonomous decision-making, perception, and
fault-tolerant operation within a traceable systems-engineering framework.

> **Current status:** DAWN v0.1.0 establishes the Project Foundation.
> Autonomous flight capabilities are planned and have not yet been implemented
> or verified.

## Project Objectives

DAWN is being developed as an end-to-end engineering project with the long-term
objective of demonstrating an autonomous UAV capable of:

- autonomous takeoff and waypoint navigation;
- state estimation from multiple sensor sources;
- detection of GNSS degradation or loss;
- degraded navigation when sufficient alternative information is available;
- autonomous continuation or safe mission termination based on defined criteria;
- designated landing-zone detection;
- autonomous approach and precision landing;
- progressive validation through simulation, SIL, and HIL.

These capabilities describe the intended project evolution and must not be
interpreted as currently implemented or verified functionality.

## Current Baseline — v0.1.0

DAWN v0.1.0 defines the engineering foundation on which later implementation
will be built.

The baseline currently contains:

- Mission Concept and operational scope;
- 27 system requirements;
- functional system architecture and responsibility allocation;
- verification strategy with one primary verification case per requirement;
- Open Engineering Decisions for criteria intentionally left unresolved;
- Python project structure and development tooling;
- automated linting and unit-test execution through CI.

All system requirements remain **Draft** and all primary verification cases
remain **Partially Defined**. No UAV capability is claimed as verified by this
release.

## Engineering Documentation

The baseline engineering documents are maintained in [`docs/`](docs/):

| Document | Purpose |
| --- | --- |
| [`01_mission_concept.md`](docs/01_mission_concept.md) | Defines the mission, operational scenarios, assumptions, scope, and success concepts. |
| [`02_system_requirements.md`](docs/02_system_requirements.md) | Defines the current system requirements and Open Engineering Decisions. |
| [`03_system_architecture.md`](docs/03_system_architecture.md) | Defines the functional architecture, responsibilities, interfaces, and system boundaries. |
| [`04_verification_matrix.md`](docs/04_verification_matrix.md) | Maps each requirement to its primary verification strategy, evidence needs, and dependencies. |

The intended traceability chain is:

```text
Mission Concept
      ↓
System Requirements
      ↓
Functional Architecture
      ↓
Verification Strategy
      ↓
Implementation and Evidence
```

## Engineering Areas

The project roadmap includes work in:

- 6-DOF flight dynamics;
- Guidance, Navigation and Control;
- sensor modelling and state estimation;
- autonomous mission management;
- computer vision and landing-zone perception;
- GNSS-degraded and GNSS-denied navigation;
- fault detection and resilient operation;
- PX4 integration;
- ROS 2 autonomy;
- Software-in-the-Loop (SIL);
- Hardware-in-the-Loop (HIL);
- systems engineering, traceability, and verification.

Technology choices listed here represent the intended development roadmap and
do not imply that each technology is already integrated.

## Repository Structure

```text
dawn-autonomous-uav/
├── .github/
│   └── workflows/          # Continuous integration
├── docs/                   # Systems-engineering baseline
├── src/
│   └── dawn/               # DAWN Python package
├── tests/                  # Automated software tests
├── AGENTS.md               # Engineering and development guidelines
├── pyproject.toml          # Python project and tool configuration
└── README.md
```

## Development Setup

DAWN currently requires Python 3.12 or later.

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install DAWN in editable mode together with the development tools:

```bash
python -m pip install -e ".[dev]"
```

Run the current software checks:

```bash
python -m ruff check .
python -m ruff format --check .
python -m pytest
```

These checks validate software formatting, linting, and automated tests. Passing
them does **not** constitute verification of DAWN system requirements.

## Development Workflow

The project follows the general workflow:

```text
Issue
  ↓
Branch
  ↓
Implementation
  ↓
Tests
  ↓
Commit
  ↓
Pull Request
  ↓
Review + CI
  ↓
Merge
```

Engineering changes should preserve traceability between requirements, design,
implementation, and verification evidence.

See [`AGENTS.md`](AGENTS.md) for the project engineering and development rules.

## Roadmap

| Phase | Development Area | Status |
| --- | --- | --- |
| v0.1 | Project Foundation | Current baseline |
| v0.2 | 6-DOF Flight Dynamics | Planned |
| v0.3 | Flight Control | Planned |
| v0.4 | State Estimation | Planned |
| v0.5 | PX4 Integration | Planned |
| v0.6 | ROS 2 Autonomy | Planned |
| v0.7 | Perception | Planned |
| v0.8 | GNSS-Degraded Navigation | Planned |
| v0.9 | Fault-Tolerant Autonomy | Planned |
| v1.0 | Integrated SIL/HIL Validation | Planned |

The roadmap is indicative and may evolve as engineering decisions are resolved.

## Author

**Ignacio Ybarra**

Aerospace Engineer