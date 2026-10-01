# DAWN Flight Dynamics Reference Model

## 1. Purpose

This document defines the mathematical conventions, assumptions,
equations of motion, numerical integration strategy, and current
verification evidence for the DAWN six-degree-of-freedom rigid-body
flight dynamics reference model.

The model is intended to provide an independent and understandable
reference implementation for:

- flight dynamics development,
- flight-control development,
- numerical experiments,
- verification of future implementations,
- comparison with PX4/SITL behavior,
- and future SIL/HIL validation activities.

The current model is a rigid-body dynamics baseline. It is not intended
to represent a complete physical UAV at this stage.

---

## 2. Model Scope

The current model includes:

- three-dimensional translational motion,
- three-dimensional rotational motion,
- quaternion attitude propagation,
- rigid-body gyroscopic coupling,
- gravitational acceleration,
- externally applied body-frame forces,
- externally applied body-frame moments,
- explicit Euler integration,
- fourth-order Runge-Kutta integration.

The current model does not yet include:

- individual rotor dynamics,
- motor or ESC dynamics,
- actuator allocation,
- aerodynamic drag,
- propeller aerodynamic models,
- wind or atmospheric disturbances,
- ground effect,
- structural flexibility,
- sensor models,
- actuator saturation,
- battery dynamics,
- Earth rotation or curvature.

These effects may be introduced later when required by DAWN system
development or verification objectives.

---

## 3. Reference Frames

### 3.1 Navigation Frame

The navigation frame uses the North-East-Down (NED) convention:

- Xn: North,
- Yn: East,
- Zn: Down.

Position and linear velocity are expressed in the NED frame.

A vehicle above the NED origin therefore has a negative Down position.

For example, a vehicle 20 m above the origin has:

p_D = -20 m

### 3.2 Body Frame

The vehicle body frame uses the Forward-Right-Down (FRD) convention:

- Xb: Forward,
- Yb: Right,
- Zb: Down.

Angular velocity, applied forces, applied moments, and the inertia
tensor are expressed in the body frame.

### 3.3 Rotation Convention

The rotation matrix R_b_n maps vector coordinates from the body frame
to the NED frame:

v_n = R_b_n v_b

The attitude quaternion follows the same body-to-navigation convention.

---

## 4. State Definition

The rigid-body state is:

x = [p_n, v_n, q_b_n, omega_b]

where:

- p_n is the vehicle center-of-mass position in NED [m],
- v_n is the vehicle center-of-mass linear velocity in NED [m/s],
- q_b_n is the body-to-NED attitude quaternion,
- omega_b is body angular velocity [rad/s].

The corresponding dimensions are:

- position: 3,
- velocity: 3,
- quaternion: 4,
- angular velocity: 3.

The numerical state therefore contains 13 variables.

The physical configuration has six degrees of freedom: three position
coordinates and three independent attitude coordinates. Adding three linear
and three angular velocity components gives 12 independent state dimensions.
The quaternion contributes four stored components but only three independent
attitude dimensions because of its unit-norm constraint. Thus the model has
6 configuration DOF, 12 independent state dimensions, and 13 stored components.

---

## 5. Quaternion Convention

DAWN uses scalar-first quaternions:

q = [w, x, y, z]

The Hamilton quaternion product is used.

The attitude quaternion is denoted q_b_n and represents the orientation
of the FRD body frame relative to the NED navigation frame.

The quaternion satisfies:

||q_b_n|| = 1

The quaternion kinematic equation is:

q_dot_b_n = 1/2 q_b_n ⊗ [0, omega_b]

where omega_b is expressed in the body frame.

The body-to-NED rotation matrix is computed directly from the
quaternion.

For a normalized quaternion:

q = [w, x, y, z]

the rotation matrix is:

```text
R_b_n =
[ 1-2(y²+z²)    2(xy-wz)      2(xz+wy)   ]
[ 2(xy+wz)      1-2(x²+z²)    2(yz-wx)   ]
[ 2(xz-wy)      2(yz+wx)      1-2(x²+y²) ]
```

The quaternions q and -q represent the same physical orientation.

Euler angles are not used as the internal attitude state.

---

## 6. Inputs

The rigid-body model receives:

u = [F_b, M_b]

where:

- F_b is the total applied non-gravitational force expressed in FRD [N],
- M_b is the total external moment about the center of mass, expressed
  in FRD [N m].

Gravity is not included in F_b.

This separation prevents gravitational force from being counted twice
and keeps the rigid-body interface independent from future actuator
models.

The current model receives forces and moments directly. It does not
receive motor commands, PWM signals, or rotor speeds.

A future actuator model may provide a mapping of the form:

motor commands
→ rotor speeds
→ rotor thrust and torque
→ total F_b and M_b
→ rigid-body dynamics

---

## 7. Translational Dynamics

Vehicle mass m is constant in the current rigid-body model.

The position kinematics are:

p_dot_n = v_n

The translational dynamics are:

v_dot_n = (1 / m) R_b_n F_b + g_n

where:

g_n = [0, 0, g]

and the current default gravitational acceleration is:

g = 9.80665 m/s²

The positive sign of the third gravity component follows directly from
the NED convention, where Down is positive.

For a level vehicle, upward rotor thrust acts in the negative body-Z
direction:

F_thrust_b = [0, 0, -T]

For level hover:

T = m g

which produces zero vertical acceleration.

---

## 8. Rotational Dynamics

Rigid-body rotational motion follows Euler's equation:

M_b = J omega_dot_b + omega_b × (J omega_b)

Therefore:

omega_dot_b =
J^(-1) [M_b - omega_b × (J omega_b)]

where J is the vehicle inertia tensor about the center of mass,
expressed in the FRD body frame. Its body-frame components are constant
in the current rigid-body model.

The implementation solves the linear system numerically rather than
explicitly computing the matrix inverse:

J omega_dot_b =
M_b - omega_b × (J omega_b)

For a diagonal inertia tensor:

J = diag(Jx, Jy, Jz)

the equations reduce to:

p_dot = [Mx + (Jy - Jz) q r] / Jx

q_dot = [My + (Jz - Jx) p r] / Jy

r_dot = [Mz + (Jx - Jy) p q] / Jz

The implementation supports a full 3x3 inertia tensor and is not
restricted to diagonal inertia matrices.

---

## 9. Complete Rigid-Body Model

The current DAWN rigid-body reference model is:

p_dot_n = v_n

v_dot_n = (1 / m) R_b_n(q_b_n) F_b + g_n

q_dot_b_n = 1/2 q_b_n ⊗ [0, omega_b]

omega_dot_b =
J^(-1) [M_b - omega_b × (J omega_b)]

This defines the continuous-time model:

x_dot = f(x, u, parameters)

---

## 10. Numerical Integration

### 10.1 Explicit Euler

An explicit Euler integrator is implemented primarily as a simple
baseline and educational reference:

x_(k+1) = x_k + x_dot_k Δt

Euler integration is not intended to be the primary high-accuracy
integration method for DAWN.

### 10.2 Fourth-Order Runge-Kutta

The primary current integrator uses classical fourth-order Runge-Kutta
(RK4) stages with the quaternion projection described in Section 10.3.

During one RK4 step, the supplied body-force and body-moment components
are held constant while the state is propagated. The body-to-NED force
transformation is reevaluated at each stage attitude, so the NED force
need not be constant. Mass, body-frame inertia, and gravity are also held
constant. A state-dependent or time-varying force model would need an
explicit stage-evaluation interface; the current input object does not
provide one.

The unconstrained RK4 formula, before applying quaternion projection, is:

For:

x_dot = f(x)

RK4 evaluates four state derivatives per integration step:

k1 = f(x_k)

k2 = f(x_k + Δt k1 / 2)

k3 = f(x_k + Δt k2 / 2)

k4 = f(x_k + Δt k3)

and computes:

x_(k+1) =
x_k + Δt (k1 + 2k2 + 2k3 + k4) / 6

### 10.3 Quaternion Normalization

Analytically, quaternion kinematics preserve unit norm.

Discretization and floating-point arithmetic can introduce norm drift.
Both integrators normalize the quaternion after propagation. Normalization
is therefore an explicit responsibility of the integration layer.

Quaternion normalization is not performed inside the rigid-body
derivative function.

The current RK4 implementation also normalizes intermediate quaternion
states used during derivative evaluation.

This is an explicit numerical design choice and means the implemented
algorithm is not a completely unconstrained textbook RK4 integration
of all 13 state variables.

Its numerical behavior is therefore evaluated through dedicated
verification studies. These provide scenario-specific evidence consistent
with approximately fourth-order behavior, not a universal proof of accuracy.

---

## 11. Verification Strategy

The dynamics reference model is checked using simple cases with known
analytical solutions or physical invariants.

Current verification cases include:

### 11.1 Free Fall

With zero applied non-gravitational force:

F_b = 0

the expected Down acceleration is:

a_D = g

For zero initial position and velocity:

v_D(t) = g t

p_D(t) = 1/2 g t²

The RK4 result is compared against this analytical solution.

### 11.2 Level Hover

For a level vehicle:

F_b = [0, 0, -m g]

the expected translational acceleration is zero.

### 11.3 Tilted Thrust

A pitched vehicle under thrust is used to verify transformation of
body-frame thrust into the NED navigation frame.

### 11.4 Applied Roll Moment

A simple principal-axis case is used to verify the expected angular
acceleration under an applied roll moment.

### 11.5 Constant Yaw Rate

For identity initial attitude q(0) = [1, 0, 0, 0] and pure constant body
yaw rate omega_b = [0, 0, r], the analytical quaternion solution is:

q(t) =
[cos(r t / 2), 0, 0, sin(r t / 2)]

This checks quaternion propagation and RK4 attitude integration. The pytest
case uses a sign-invariant angular distance in radians and a 1e-6 rad
accuracy budget for r = 1 rad/s, dt = 0.1 s, and a 1 s horizon. This permits
margin above the usual RK4 leading phase-error scale (about 5.2e-8 rad)
while excluding normalized Euler's approximately 8.3e-4 rad error for the
same scenario. It is a numerical regression budget, not a flight requirement.

A separate noncommuting convention test applies a body roll rate to an
initial +90-degree yaw attitude to distinguish right from left Hamilton
multiplication in the quaternion derivative.

### 11.6 Gyroscopic Coupling

Torque-free rotation with nonzero angular velocity and unequal
principal moments of inertia is used to verify the gyroscopic term:

omega_b × (J omega_b)

A full-inertia regression also transforms a known principal-axis inertia,
angular velocity, and applied moment into FRD with an independent orthogonal
rotation. Its expected acceleration comes from the scalar principal-axis
Euler equations, then the same coordinate change. This covers non-diagonal
inertia without constructing the expectation from the production solver.

### 11.7 Torque-Free Conservation

For torque-free rigid-body rotation:

M_b = 0

the rotational kinetic energy:

E_rot = 1/2 omega_b^T J omega_b

should remain constant.

The inertial angular momentum:

H_n = R_b_n J omega_b

should also remain constant.

These invariants are monitored throughout the simulation rather than
only at the final time. A bounded pytest regression uses the Section 12
fixture at dt = 0.05 s for 5 s, checking every propagated sample. Relative
error budgets are 1e-6 for energy and 1e-5 for inertial angular momentum,
providing modest margin over the measured 1.810e-7 and 2.681e-6 errors.
These bounds guard numerical behavior and do not assert exact conservation.
The convergence sweep remains a separate numerical study.

---

## 12. RK4 Convergence Study

A torque-free rigid-body rotation case was simulated for 5 seconds
using the following integration time steps:

- 0.1000 s,
- 0.0500 s,
- 0.0250 s,
- 0.0125 s.

The maximum relative rotational-energy error and maximum relative
inertial-angular-momentum error were measured during each simulation.

| Time step [s] | Max relative energy error | Max relative angular momentum error |
|---:|---:|---:|
| 0.1000 | 5.143e-06 | 4.367e-05 |
| 0.0500 | 1.810e-07 | 2.681e-06 |
| 0.0250 | 8.981e-09 | 1.659e-07 |
| 0.0125 | 6.048e-10 | 1.031e-08 |

The observed convergence orders were:

| Time-step refinement [s] | Energy order | Angular momentum order |
|---:|---:|---:|
| 0.1000 → 0.0500 | 4.828 | 4.026 |
| 0.0500 → 0.0250 | 4.333 | 4.014 |
| 0.0250 → 0.0125 | 3.892 | 4.009 |

The angular-momentum conservation error exhibits approximately
fourth-order convergence across all tested refinements.

The rotational-energy conservation error also decreases rapidly and
shows behavior consistent with approximately fourth-order convergence
over the tested range.

These results provide numerical evidence consistent with the expected
behavior of the RK4 integration scheme for the current torque-free
rotation case.

They do not constitute a general mathematical proof of fourth-order
accuracy for every possible DAWN simulation scenario.

---

## 13. Test Parameters

Simple masses, inertia tensors, angular velocities, forces, and moments
used in unit tests and numerical verification studies are analytical
test fixtures.

They are selected to make expected physical behavior easy to calculate
and verify.

They are not claimed to represent the final physical parameters of a
DAWN UAV.

Physical vehicle parameters will be introduced only when a specific
vehicle configuration has been defined and justified.

### 13.1 Parameter Validation and Physical Realizability

`VehicleParameters` checks positive finite mass and a finite 3x3 inertia
tensor that is approximately symmetric and positive definite. These checks
establish numerical admissibility for the rigid-body equations, not proof
of a physically realizable mass distribution.

Physical principal moments additionally satisfy the inertia triangle
inequalities:

```text
Jx + Jy >= Jz
Jy + Jz >= Jx
Jz + Jx >= Jy
```

For example, diag(1, 1, 3) [kg m²] is SPD and accepted numerically, but
violates Jx + Jy >= Jz and cannot represent a physical rigid-body inertia.
The nominal analytical fixtures used in the tests and studies satisfy
these relationships, including the rotated non-diagonal fixture. Deliberately
invalid validation-test inputs are not physical parameter examples.

Physical vehicle-parameter ingestion in a later milestone should enforce
or independently establish realizability. No triangle-inequality enforcement
is added in v0.2.

### 13.2 Array Ownership and Validation Lifetime

`RigidBodyState`, `ForcesMoments`, and `VehicleParameters` convert array
inputs to independent float64 copies. Mutating an original caller-owned
array therefore does not change the constructed object. The rigid-body
derivative also returns a position-derivative array independent of the
state velocity.

Validation occurs at construction. Fields remain mutable, and direct
assignment or in-place mutation of stored fields is not revalidated.
Callers must preserve shapes, finite values, quaternion unit norm, and
parameter validity. These objects are not immutable containers.

---

## 14. Current Limitations

The current reference model represents ideal rigid-body motion under
specified forces and moments.

It does not yet represent the complete dynamics of a multirotor UAV.

In particular, the model currently assumes that total body forces and
moments are already known.

Future model extensions may introduce:

- actuator and rotor models,
- force and moment allocation,
- aerodynamic effects,
- environmental disturbances,
- actuator limits,
- vehicle-specific physical parameters.

Model complexity should only be increased when required by a defined
engineering or verification objective.

---

## 15. Verification Status

The current automated tests and numerical studies provide evidence for
the implemented mathematical behavior of the rigid-body reference
model.

Passing these tests does not by itself verify DAWN system-level
requirements, flight safety, physical vehicle fidelity, or future
closed-loop performance.

The model provides the ideal rigid-body reference baseline for DAWN v0.2.0.
Physical vehicle modeling and closed-loop capabilities belong to later milestones.

---

## 16. Reproducing the Numerical Studies

From the repository root, use the Python 3.12-or-later development environment
and install the package with its analysis tools if needed:

```bash
python -m pip install -e ".[dev]"
python scripts/compare_integrators.py
python scripts/visualize_torque_free_rotation.py
python scripts/analyze_rk4_convergence.py
```

For a headless environment, set `MPLBACKEND=Agg` before running the scripts.
Each script creates `results/figures/` if needed and overwrites its own PNG.

| Script | Output under `results/figures/` | Fixture and horizon |
| --- | --- | --- |
| `compare_integrators.py` | `free_fall_integrator_comparison.png` | m = 1 kg, J = diag(1, 1, 1) kg m², omega(0) = 0, g = 9.80665 m/s², dt = 0.1 s, duration = 1 s |
| `visualize_torque_free_rotation.py` | `torque_free_rotation_validation.png` | m = 1 kg, J = diag(0.2, 0.3, 0.4) kg m², omega(0) = [1, 2, 3] rad/s, g = 0, dt = 0.01 s, duration = 5 s |
| `analyze_rk4_convergence.py` | `rk4_convergence_study.png` | Same torque-free fixture, duration = 5 s, dt = 0.1, 0.05, 0.025, 0.0125 s |

All studies start at zero NED position and velocity with identity
body-to-NED attitude, zero non-gravitational body force, and zero body
moment. These are analytical/numerical fixtures, **not final physical DAWN
vehicle parameters**. The torque-free fixture starts with E_rot = 2.5 J
and H_n = [0.2, 0.6, 1.2] kg m²/s.

The torque-free visualization prints maximum absolute invariant errors;
the convergence study prints maximum relative errors and observed orders.
Section 12 records the convergence results. The visualization title reads
"Numerical Verification"; its existing filename is retained for continuity
and does not imply physical validation.

The pre-release evidence was reproduced on Linux with Python 3.12.3,
NumPy 2.5.3, and Matplotlib 3.11.2, using the Agg plotting backend. These
versions record an observed environment, not dependency pins or guarantees
of identical PNG rendering across platforms. Inspect the active environment
with:

```bash
python --version
python -m pip show numpy matplotlib
```

The three milestone figures may be retained in version control alongside
the scripts and documented numerical results. Structured histories and
machine-readable metrics remain a future improvement. These studies verify
mathematical/numerical behavior only; they do not validate physical vehicle
fidelity or satisfy system-level requirements.
