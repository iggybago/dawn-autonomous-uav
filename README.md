# DAWN

## Resilient Autonomous UAV Engineering Project

DAWN is a personal aerospace engineering project focused on the progressive
development, simulation, integration, and validation of a resilient autonomous
unmanned aerial vehicle.

The project is intended to integrate flight dynamics, Guidance, Navigation and
Control (GNC), state estimation, autonomous decision-making, perception, and
fault-tolerant operation within a traceable systems-engineering framework.

> **Current status:** DAWN v0.2.0 — 6-DOF Flight Dynamics.
> A Python rigid-body reference model with analytical and numerical verification
> evidence. Autonomous flight capabilities remain planned.

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

## Current Baseline — v0.2.0

DAWN v0.2 introduces an ideal, open-loop 6-DOF rigid-body flight-dynamics
reference model in Python. Its implemented scope includes:

- NED (North-East-Down) navigation and FRD (Forward-Right-Down) body frames,
  with SI units and angles in radians;
- 13 stored state components: center-of-mass position and velocity, a unit
  attitude quaternion, and body angular velocity;
- scalar-first Hamilton quaternions representing body-to-NED orientation,
  with `vector_n = R_b_n @ vector_b`;
- translational and rotational dynamics, including gyroscopic coupling and
  full 3x3 body-frame inertia, driven by prescribed non-gravitational body
  forces and moments about the center of mass; gravity is handled separately;
- explicit Euler as a baseline and RK4 as the primary integrator, with
  quaternion normalization after propagation and at intermediate RK4 stages;
- construction-time parameter, state, and input validation, with independent
  copies of caller-provided arrays;
- automated pytest regressions and reproducible numerical studies.

Six configuration degrees of freedom correspond to 12 independent state
dimensions; the unit quaternion accounts for the thirteenth stored component.
The model is an engineering reference, not a complete multirotor simulation.
Rotor/motor/ESC models, aerodynamics, flight controllers, and state estimation
are outside this milestone. PX4, ROS 2, perception, autonomous mission management,
GNSS-denied navigation, and FDIR implementations remain future work. No physical
UAV validation is claimed.

The v0.1 Project Foundation is retained: mission concept, 27 system requirements,
functional architecture, verification planning, and Open Engineering Decisions.
All system requirements remain **Draft** and all primary verification cases
remain **Partially Defined**. Numerical model verification does not establish
system-level requirement satisfaction.

## Engineering Documentation

The baseline engineering documents are maintained in [`docs/`](docs/):

| Document | Purpose |
| --- | --- |
| [`01_mission_concept.md`](docs/01_mission_concept.md) | Defines the mission, operational scenarios, assumptions, scope, and success concepts. |
| [`02_system_requirements.md`](docs/02_system_requirements.md) | Defines the current system requirements and Open Engineering Decisions. |
| [`03_system_architecture.md`](docs/03_system_architecture.md) | Defines the functional architecture, responsibilities, interfaces, and system boundaries. |
| [`04_verification_matrix.md`](docs/04_verification_matrix.md) | Maps each requirement to its primary verification strategy, evidence needs, and dependencies. |
| [`05_flight_dynamics_model.md`](docs/05_flight_dynamics_model.md) | Details the flight-dynamics equations, conventions, assumptions, numerical verification, and reproduction instructions. |

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

## Analytical and Numerical Evidence

The pytest suite covers analytical free fall, level hover force balance,
tilted thrust, applied moments, full-inertia dynamics, quaternion conventions,
attitude propagation, torque-free conservation, and input/ownership regressions.
The current release candidate passes 58 local tests.

Three reproducible studies complement those regressions:

| Study | Script | Generated figure |
| --- | --- | --- |
| Euler and RK4 against analytical free fall | [`compare_integrators.py`](scripts/compare_integrators.py) | [Free-fall comparison](results/figures/free_fall_integrator_comparison.png) |
| Torque-free energy and inertial angular momentum conservation | [`visualize_torque_free_rotation.py`](scripts/visualize_torque_free_rotation.py) | [Conservation evidence](results/figures/torque_free_rotation_validation.png) |
| RK4 timestep refinement | [`analyze_rk4_convergence.py`](scripts/analyze_rk4_convergence.py) | [Convergence evidence](results/figures/rk4_convergence_study.png) |

The convergence study is consistent with approximately fourth-order behavior
for the tested torque-free scenario. These results support mathematical and
numerical verification; they do not prove accuracy for every scenario, physical
vehicle fidelity, or closed-loop flight performance. Experiment parameters are
analytical fixtures, not final DAWN vehicle parameters.

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
├── docs/                   # Systems engineering and dynamics model
├── results/
│   └── figures/            # Reproducible milestone figures
├── scripts/                # Numerical verification studies
├── src/
│   └── dawn/
│       └── dynamics/       # Rigid-body model and integrators
├── tests/
│   └── dynamics/           # Physics and input-validation regressions
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
python -m ruff format --check .
python -m ruff check .
python -m pytest
```

These checks validate software formatting, linting, and automated tests. Passing
them does **not** constitute verification of DAWN system requirements.

To regenerate the numerical studies and their figures from the repository root:

```bash
python scripts/compare_integrators.py
python scripts/visualize_torque_free_rotation.py
python scripts/analyze_rk4_convergence.py
```

The development extra includes Matplotlib for these scripts; NumPy is a runtime
dependency. In a headless environment, set `MPLBACKEND=Agg`. Outputs are written
to [`results/figures/`](results/figures/).

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
| v0.1 | Project Foundation | Completed |
| v0.2 | 6-DOF Flight Dynamics | Completed — current milestone |
| v0.3 | Flight Control | Next |
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