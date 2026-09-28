# DAWN Mission Concept

## 1. Purpose and Baseline

DAWN is a personal aerospace engineering and learning project for developing
and validating a resilient autonomous multirotor UAV. Its mission objective
is to demonstrate autonomous mission completion under nominal conditions
and an appropriate response to navigation degradation, including safe
termination when continued operation is not appropriate.

This initial Mission Concept baseline is simulation-first. It defines the
mission intent and scope from which system requirements will be derived.
Engineering understanding, traceability and reproducible validation are
central project objectives.

## 2. Project Roles

A single person may perform multiple roles:

- **Developer / systems engineer:** defines mission needs, derives
  requirements and develops the system while maintaining traceability.
- **Test and validation engineer:** defines test scenarios and evaluates
  evidence against mission success criteria and derived requirements.
- **Mission supervisor / operator:** prepares and authorizes the mission,
  supervises safety and may terminate a test when necessary.

## 3. System Boundary and Mission Capabilities

DAWN encompasses the autonomous UAV functions needed to perform the mission
and their interfaces:

- **Navigation and state estimation:** determine vehicle motion and position
  using available information, including during GNSS degradation or loss.
- **Guidance and control:** maintain stable flight and execute takeoff,
  waypoint navigation, approach and precision landing.
- **Autonomy:** manage mission progression and decide whether to continue
  or terminate the mission.
- **Perception:** search for and identify the designated landing zone.
- **Health monitoring and fault handling:** detect navigation degradation,
  assess continued operation and manage the appropriate response.

External elements are:

- **Navigation services:** provide external navigation information, including
  Global Navigation Satellite System (GNSS) information; availability may
  change during a degraded scenario.
- **Operating environment:** provides the flight area, environmental
  conditions and designated landing zone with which the UAV interacts.
- **Mission supervision:** supplies the mission definition and authorization,
  receives mission status and provides safety or test-termination direction.
- **Development and validation infrastructure:** represents the vehicle and
  environment in simulation, introduces test faults and collects evidence.

These are functional boundaries; allocation to software, hardware or
specific technologies is deferred to architecture and design.

## 4. Reference Scenario and Nominal Mission

The reference mission takes place in a defined simulated test environment.
A predefined waypoint route leads to a search for a designated landing
zone, followed by approach and landing. The mission definition and test
conditions are established before execution.

The nominal sequence is:

1. System initialization.
2. Pre-flight checks to establish readiness to proceed.
3. Autonomous takeoff.
4. Navigation through the predefined waypoints.
5. Search for and identification of the designated landing zone.
6. Autonomous approach to the identified landing zone.
7. Precision landing at the designated zone.
8. Mission completion.

Required systems and navigation information remain nominal throughout this
scenario. GNSS degradation or loss is not part of the nominal mission.

## 5. Initial Degraded Mission Scenarios

The initial degraded baseline covers GNSS degradation or loss during the
reference mission. Each scenario introduces a navigation-service fault
under defined test conditions. The autonomous system is expected to:

1. Detect the navigation degradation.
2. Assess whether available navigation information and system capability
   support continued operation.
3. Transition to degraded operation when continuation is appropriate.
4. Continue the mission using available alternative navigation information,
   or execute a predefined safe termination behavior when continued
   operation is not appropriate.

Continued operation remains conditional on the system's ability to perform
the mission safely. Safe termination ends mission pursuit and brings the
vehicle to a defined safe terminal state. The applicable behavior, terminal
state and conditions for continuation or termination will be specified in
system requirements and test definitions before validation.

## 6. Mission Success Criteria

- **Successful nominal completion:** the UAV completes the nominal sequence,
  maintains controlled flight and lands at the designated zone without
  human intervention in mission execution.
- **Successful degraded completion:** the UAV detects GNSS degradation or
  loss, appropriately transitions to degraded operation and completes the
  remaining mission, including landing at the designated zone, without
  human intervention in mission execution.
- **Successful resilience demonstration through safe termination:** the UAV
  detects navigation degradation, determines that continuation is not
  appropriate and autonomously executes the predefined safe termination
  behavior, reaching the defined safe terminal state. This demonstrates
  resilience but does not constitute completion of the planned mission.

Supervisor intervention or test termination alone does not demonstrate a
successful autonomous response. Recorded evidence must support the claimed
outcome against derived requirements and the applicable test conditions.

Measurable thresholds for precision landing, tracking accuracy and
fault-detection performance will be defined in
[system requirements](02_system_requirements.md). This concept assigns no
numerical performance thresholds and makes no claim of achieved verification.

## 7. Assumptions and Constraints

- The vehicle starts in a valid initial state.
- Required systems are nominal at mission start unless a test explicitly
  injects a fault; fault-injection cases are degraded scenarios.
- The mission operates within a defined test environment with an established
  route, landing-zone designation and operating conditions.
- The nominal mission assumes navigation information is initially available
  and remains available during execution.
- Human intervention is not expected during autonomous mission execution,
  except for safety supervision or test termination.
- The initial demonstration is simulation-based. Software-in-the-Loop (SIL),
  Hardware-in-the-Loop (HIL) and physical flight testing may be introduced
  in later validation phases; none is required to define this initial mission.

## 8. Future Extensions and Exclusions

IMU bias or excessive sensor noise, barometer failure, camera loss,
communication loss, motor degradation and low battery are future fault
extensions and are outside the initial degraded baseline.

The initial mission baseline also excludes:

- Multi-UAV or swarm operation.
- Operation in uncontrolled real-world airspace.
- Certification.
- Fully general obstacle avoidance.
- Simultaneous multiple-fault scenarios.
- Production hardware design.
