# AGENTS.md — DAWN Engineering Guidelines

## 1. Project Overview

DAWN is a personal aerospace engineering project focused on the design,
simulation, implementation and validation of a resilient autonomous
multirotor UAV.

The project is intended both as an engineering system and as a learning
platform. Code quality alone is not sufficient: implementations must be
physically meaningful, understandable, testable and traceable to engineering
requirements.

The project will progressively integrate:

- 6-DOF flight dynamics
- Guidance, Navigation and Control (GNC)
- Sensor modelling
- State estimation and sensor fusion
- PX4 autopilot integration
- ROS 2
- Autonomous mission management
- Computer vision
- GNSS-denied navigation
- Fault Detection, Isolation and Recovery (FDIR)
- Software-in-the-Loop (SIL)
- Hardware-in-the-Loop (HIL)
- Systems engineering and verification

The long-term objective is to demonstrate an autonomous UAV mission under
both nominal and degraded operating conditions.

---

## 2. Engineering Priorities

When making engineering or software decisions, use the following priorities:

1. Physical and mathematical correctness
2. Safety and deterministic behaviour
3. Testability and verification
4. Readability and maintainability
5. Requirements traceability
6. Reproducibility
7. Performance

Do not sacrifice correctness or clarity for premature optimization.

---

## 3. Learning-Oriented Development

DAWN is a learning-focused engineering project.

Do not hide important engineering decisions behind unnecessary abstractions
or unexplained generated code.

When implementing a significant algorithm, especially in:

- flight dynamics
- control
- guidance
- navigation
- estimation
- sensor fusion
- coordinate transformations
- autonomy
- fault detection

the implementation must make the underlying engineering logic understandable.

For significant mathematical implementations:

1. State the mathematical model or algorithm being implemented.
2. Define variables and units.
3. Define coordinate frames and sign conventions.
4. State relevant assumptions.
5. Reference the associated requirement when available.
6. Add tests that demonstrate expected behaviour.

Prefer clear implementations that can be reviewed and explained by an
aerospace engineer over unnecessarily clever code.

---

## 4. Coordinate Frames and Conventions

Coordinate-frame conventions are safety-critical project decisions.

Unless a module explicitly documents otherwise:

### World / Navigation Frame

Use NED:

- X: North
- Y: East
- Z: Down

### Body Frame

Use FRD:

- X: Forward
- Y: Right
- Z: Down

### Units

Use SI units unless explicitly documented otherwise.

Examples:

- distance: m
- velocity: m/s
- acceleration: m/s²
- mass: kg
- force: N
- torque: N·m
- angular velocity: rad/s
- angles: rad
- time: s

Never mix degrees and radians implicitly.

Never introduce a coordinate transformation without documenting:

- source frame
- destination frame
- rotation convention
- quaternion convention, if applicable

Do not silently change coordinate-frame or quaternion conventions.

---

## 5. Flight Dynamics and GNC Rules

Flight dynamics and GNC code must prioritize mathematical transparency.

For dynamics models:

- Document state-vector definitions and ordering.
- Document input-vector definitions and ordering.
- Document force and moment conventions.
- Document reference frames.
- Document assumptions.
- Keep physical parameters explicit and configurable.
- Avoid unexplained magic constants.

For controllers:

- Clearly distinguish guidance, control and actuator logic.
- Document controller inputs and outputs.
- Document saturation limits.
- Consider actuator saturation explicitly.
- Implement anti-windup where relevant.
- Make controller gains configurable.
- Add tests for nominal and boundary conditions.

When implementing equations from literature or documentation, reference the
source in code comments or project documentation when practical.

---

## 6. State Estimation Rules

State-estimation code must explicitly document:

- state vector
- process model
- measurement model
- covariance definitions
- process noise assumptions
- measurement noise assumptions
- coordinate frames
- units

For Kalman-filter-based estimators, keep prediction and correction logic
clearly identifiable.

Do not tune estimator parameters solely to make a test pass without explaining
the engineering justification.

Sensor failures, biases and noise should eventually be testable through
fault injection.

---

## 7. Software Architecture

Prefer modular components with clear responsibilities.

Avoid tightly coupling:

- vehicle dynamics
- controllers
- estimators
- sensor models
- mission logic
- perception
- communication interfaces

The architecture should progressively support replacing simulated components
with real implementations.

For example:

simulated sensors -> PX4 sensors -> real hardware

without requiring unnecessary redesign of unrelated modules.

Public interfaces should be explicit and documented.

---

## 8. Python Guidelines

Python code should:

- follow modern Python practices
- use type hints where useful
- use descriptive names
- keep functions reasonably small
- avoid unnecessary dependencies
- include docstrings for public interfaces
- be compatible with the Python version defined by the project

Use Ruff for linting and formatting checks.

Use pytest for Python testing.

Do not suppress linting or type issues merely to make automated checks pass
unless there is a documented reason.

---

## 9. C++ Guidelines

When C++ is introduced:

- prefer modern C++
- use RAII
- avoid unnecessary manual memory management
- use const correctness
- keep ownership explicit
- prefer deterministic behaviour
- use CMake as the build system

Use GoogleTest or the testing framework selected by the project.

Avoid adding complex template abstractions unless they provide a clear
engineering benefit.

---

## 10. ROS 2 Guidelines

When ROS 2 is introduced:

- keep nodes focused on clear responsibilities
- document topics, services and actions
- document message types
- document coordinate frames
- use TF2 consistently
- define QoS deliberately rather than relying blindly on defaults

ROS 2 interfaces should be documented as part of the DAWN system architecture.

Do not embed core flight-dynamics or estimation mathematics directly inside
ROS communication code when it can be implemented and tested independently.

---

## 11. PX4 Integration

PX4 should be treated as an external flight-control system with explicit
interfaces.

Clearly document:

- information sent to PX4
- information received from PX4
- MAVLink/MAVSDK interfaces
- coordinate conversions
- timing assumptions
- operating modes

PX4-specific code should not unnecessarily contaminate generic DAWN algorithms.

Whenever possible, algorithms should remain independently testable without
launching the complete PX4 simulation.

---

## 12. Testing Philosophy

New functionality should normally include tests.

Use the lowest appropriate test level:

1. Unit tests
2. Component tests
3. Integration tests
4. Simulation tests
5. SIL tests
6. HIL tests

Tests should verify engineering behaviour rather than implementation details
whenever practical.

Important algorithms should include:

- nominal cases
- boundary cases
- invalid inputs where relevant
- degraded or failure cases where relevant

Never:

- delete a failing test simply to make CI pass
- weaken acceptance criteria without documenting why
- change expected numerical results without understanding the reason
- hide test failures

Numerical tests must use physically justified tolerances.

---

## 13. Verification and Requirements

DAWN follows a requirements-driven development approach.

Requirements are maintained in:

docs/02_system_requirements.md

Verification information is maintained in:

docs/04_verification_matrix.md

When implementing functionality associated with a requirement:

- reference the requirement ID where practical
- identify how the implementation will be verified
- update verification documentation when appropriate

Verification methods may include:

- Analysis
- Inspection
- Simulation
- Test
- Demonstration
- Fault Injection Test

Do not mark a requirement as verified unless objective evidence exists.

---

## 14. Fault Handling and Safety

Fault-tolerant behaviour is a core DAWN objective.

Future implementations should support testing failures such as:

- GNSS loss or degradation
- sensor bias
- excessive sensor noise
- barometer failure
- camera loss
- communication loss
- motor degradation
- low battery conditions

Failure handling should distinguish between:

- fault detection
- fault isolation
- degraded operation
- recovery
- safe mission termination

Do not silently ignore invalid sensor data or critical failures.

---

## 15. Documentation

Documentation is part of the engineering product.

Update documentation when a change affects:

- architecture
- interfaces
- assumptions
- coordinate frames
- requirements
- verification strategy
- setup instructions

Use Mermaid diagrams where appropriate for architecture and data-flow diagrams.

Important mathematical models should be documented independently from their
software implementation.

---

## 16. Git Workflow

Use small, focused changes.

Preferred workflow:

Issue
-> Branch
-> Implementation
-> Tests
-> Commit
-> Pull Request
-> Review
-> CI
-> Merge

Do not make unrelated changes in the same task.

Suggested commit prefixes:

- feat:
- fix:
- docs:
- test:
- refactor:
- chore:
- ci:

Examples:

feat: implement quaternion rotation utilities

test: add NED to body transformation tests

docs: define initial navigation requirements

fix: correct body-frame acceleration sign

---

## 17. Working Procedure for AI Agents

Before modifying the repository:

1. Inspect the relevant existing files.
2. Understand the requested task.
3. Identify relevant requirements.
4. Identify affected modules and tests.
5. Avoid modifying unrelated files.

For substantial engineering changes, provide a short implementation plan
before editing.

After making changes:

1. Review the diff.
2. Run the relevant formatter/linter.
3. Run relevant unit tests.
4. Run broader tests when appropriate.
5. Report exactly which checks were executed.
6. Report any checks that could not be executed.
7. Summarize engineering assumptions introduced by the change.

Do not claim that code works unless appropriate validation has actually been
executed.

---

## 18. Commands

As the project evolves, prefer repository-defined commands over ad-hoc
alternatives.

For the current Python development environment, expected checks include:

```bash
ruff check .
pytest
```
