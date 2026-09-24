# DAWN System Requirements

## Baseline and Conventions

This initial requirements baseline derives from the
[DAWN Mission Concept](01_mission_concept.md). All requirements have status
**Draft**. Verification methods are proposed; no requirement is claimed as
verified. Open decisions must be resolved before the affected acceptance
criteria can be finalized.

`MC §` identifies a Mission Concept section. Requirement IDs in the
Parent / source column identify parent requirements. `OE-xxx` references
identify unresolved definitions or acceptance criteria in Open Engineering
Decisions; dependencies also apply through parent and referenced requirements.

The baseline is simulation-first. Fault Injection Test refers only to
simulated GNSS degradation or loss. Mission Concept assumptions remain test
preconditions, and its exclusions remain outside this baseline. Functional
categories do not allocate responsibilities to implementation technologies.

MIS-002 requires conditional mission continuation. MIS-003 defines the
complementary safe-termination outcome. Continuation alone does not establish
successful degraded mission completion: that outcome still requires completion
of the remaining mission under MC §6. Safe termination demonstrates resilience
without constituting completion of the planned mission.

## MIS — Mission

| ID | Title | Requirement statement | Parent / source | Verification method | Status |
| --- | --- | --- | --- | --- | --- |
| MIS-001 | Nominal mission completion | DAWN shall autonomously complete the reference nominal mission under the defined nominal test conditions. | MC §§4, 6 | Simulation — end-to-end nominal mission; OE-003, OE-020, OE-021. | Draft |
| MIS-002 | Degraded mission continuation | DAWN shall autonomously continue the reference mission following GNSS degradation or loss when the defined conditions for continued operation are satisfied. | MC §§5, 6 | Fault Injection Test — continuation scenarios; OE-013, OE-014, OE-020, OE-021. | Draft |
| MIS-003 | Resilient termination outcome | DAWN shall autonomously reach the defined safe terminal state when GNSS degradation or loss makes continued mission operation inappropriate according to the continuation criteria. | MC §§5, 6 | Fault Injection Test — termination scenarios; OE-014, OE-015, OE-020, OE-021. | Draft |

## SYS — System

| ID | Title | Requirement statement | Parent / source | Verification method | Status |
| --- | --- | --- | --- | --- | --- |
| SYS-001 | Mission information input | DAWN shall accept the mission information required to execute the predefined waypoint route and designated landing objective. | MC §§3, 4, 7 | Test — acceptance of mission information; OE-017. | Draft |
| SYS-002 | System initialization | DAWN shall establish the defined initialized system state before commencing pre-flight checks. | MIS-001; MC §4, step 1 | Test — initialization completion; OE-001. | Draft |
| SYS-003 | Pre-flight readiness assessment | DAWN shall determine readiness to proceed by evaluating the defined pre-flight checks. | MIS-001; MC §4, step 2 | Test — ready and not-ready conditions; OE-002. | Draft |
| SYS-004 | Mission status availability | DAWN shall make its current mission status available for mission supervision. | MC §3, mission supervision | Test — status availability across mission phases; OE-018. | Draft |

## GNC — Guidance, Navigation and Control

| ID | Title | Requirement statement | Parent / source | Verification method | Status |
| --- | --- | --- | --- | --- | --- |
| GNC-001 | Flight stability | DAWN shall maintain vehicle flight stability throughout airborne mission execution within the defined test conditions. | MC §§3, 6 | Simulation — stability across applicable mission scenarios; OE-004, OE-020. | Draft |
| GNC-002 | Autonomous takeoff | DAWN shall perform takeoff autonomously from the defined launch condition to the defined takeoff-completion condition. | MIS-001; MC §4, step 3 | Simulation — takeoff; OE-003, OE-020. | Draft |
| GNC-003 | Waypoint navigation | DAWN shall navigate through the predefined waypoint sequence in its specified order, satisfying the waypoint tracking and acceptance criteria. | MIS-001; MC §4, step 4; MC §6 | Simulation — route execution; OE-005. | Draft |
| GNC-004 | Autonomous approach | DAWN shall autonomously execute the approach to the identified designated landing zone. | MIS-001; MC §4, step 6 | Simulation — approach to an identified zone; OE-003, OE-020. | Draft |
| GNC-005 | Precision landing | DAWN shall autonomously land at the designated landing zone in accordance with the precision-landing acceptance criteria. | MIS-001, MIS-002; MC §§4, 6 | Simulation — landing against zone reference and acceptance criteria; OE-008. | Draft |

## EST — State Estimation / Navigation

| ID | Title | Requirement statement | Parent / source | Verification method | Status |
| --- | --- | --- | --- | --- | --- |
| EST-001 | Vehicle state estimation | DAWN shall estimate vehicle position and motion from available navigation information in accordance with the state-estimation acceptance criteria. | MC §3, navigation and state estimation | Simulation — estimates compared with simulation reference state; OE-006. | Draft |
| EST-002 | Degraded navigation | DAWN shall provide vehicle position and motion estimates using alternative navigation information during degraded operation, including GNSS-unavailable conditions, in accordance with the degraded-navigation acceptance criteria. | MIS-002; MC §§3, 5 | Fault Injection Test — degraded estimates compared with simulation reference state; OE-013. | Draft |

## AUT — Autonomous Mission Management

| ID | Title | Requirement statement | Parent / source | Verification method | Status |
| --- | --- | --- | --- | --- | --- |
| AUT-001 | Mission authorization | DAWN shall commence autonomous mission execution only after receiving mission authorization from mission supervision. | MC §§2, 3 | Test — authorization present and absent; OE-019. | Draft |
| AUT-002 | Takeoff readiness gate | DAWN shall initiate takeoff only when the pre-flight readiness assessment permits proceeding. | SYS-003; MC §4, steps 2–3 | Test — takeoff permitted and inhibited; OE-002. | Draft |
| AUT-003 | Nominal phase progression | DAWN shall progress through the nominal mission phases in the order defined in MC §4, advancing only when the current phase's completion criteria are satisfied. | MIS-001; MC §§3, 4 | Simulation — phase transitions; OE-003. | Draft |
| AUT-004 | Continuation assessment | Following detection of GNSS degradation or loss, DAWN shall assess whether available navigation information and system capability satisfy the conditions for continued operation. | MC §5, step 2 | Fault Injection Test — conditions permitting and preventing continuation; OE-014. | Draft |
| AUT-005 | Continuation or termination selection | DAWN shall select mission continuation when the continuation assessment permits it and safe termination otherwise. | AUT-004; MC §5, step 4 | Test — decision outcomes for both assessment results; OE-014. | Draft |
| AUT-006 | Transition to degraded operation | DAWN shall transition to degraded operation when mission continuation is selected following detection of GNSS degradation or loss. | AUT-005; MC §5, step 3 | Fault Injection Test — degraded-operation transition; OE-003, OE-013. | Draft |

## PER — Perception

| ID | Title | Requirement statement | Parent / source | Verification method | Status |
| --- | --- | --- | --- | --- | --- |
| PER-001 | Landing-zone search | DAWN shall autonomously search for the designated landing zone during the landing-zone acquisition phase within the defined search conditions. | MIS-001; MC §§3, 4, step 5 | Simulation — landing-zone search scenarios; OE-007, OE-020. | Draft |
| PER-002 | Landing-zone identification | DAWN shall identify the designated landing zone in accordance with the landing-zone identification criteria before commencing approach. | MIS-001; MC §4, steps 5–6 | Simulation — identification and approach sequencing; OE-007. | Draft |

## SAF — Safety / Resilience

| ID | Title | Requirement statement | Parent / source | Verification method | Status |
| --- | --- | --- | --- | --- | --- |
| SAF-001 | GNSS degradation detection | DAWN shall detect GNSS degradation in accordance with the defined degradation and detection-performance criteria. | MC §5, step 1; MC §6 | Fault Injection Test — degraded GNSS information; OE-010, OE-012. | Draft |
| SAF-002 | GNSS loss detection | DAWN shall detect GNSS loss in accordance with the defined loss and detection-performance criteria. | MC §5, step 1; MC §6 | Fault Injection Test — unavailable GNSS information; OE-011, OE-012. | Draft |
| SAF-003 | Safe termination execution | DAWN shall autonomously execute the predefined safe termination behavior when safe termination is selected. | MIS-003, AUT-005; MC §§5, 6 | Fault Injection Test — termination behavior; OE-015. | Draft |
| SAF-004 | End mission pursuit | DAWN shall cease pursuit of the planned mission objectives when safe termination is selected. | AUT-005; MC §5 | Test — mission progression after termination selection; OE-003, OE-015. | Draft |
| SAF-005 | Supervisor safety intervention | DAWN shall respond to mission-supervisor safety or test-termination direction in accordance with the defined supervisory response rules. | MC §§2, 3, 7 | Test — supervisory direction and resulting response; OE-016. | Draft |

## Open Engineering Decisions

These entries record decisions still needed, not additional requirements or
selected designs. Their resolution must remain consistent with the Mission
Concept. No numerical acceptance thresholds are assigned in this baseline.

| ID | Topic | Decision required |
| --- | --- | --- |
| OE-001 | Initialization completion | Define the initialized system state and observable initialization-completion criteria before pre-flight checks. |
| OE-002 | Pre-flight readiness | Define the required checks, readiness outcomes and criteria permitting takeoff. |
| OE-003 | Mission-phase transitions | Define phase entry and completion criteria, including launch, takeoff completion, approach completion, mission completion and the transition to degraded operation or termination. |
| OE-004 | Flight stability | Define nominal flight-stability acceptance criteria and their applicability during degraded operation and safe termination. |
| OE-005 | Waypoint acceptance | Define waypoint attainment, route progression and tracking-accuracy acceptance criteria. |
| OE-006 | State-estimation performance | Define the position and motion quantities to be assessed, reference conventions and estimation-performance acceptance criteria. |
| OE-007 | Landing-zone acquisition | Define the landing-zone designation, search conditions and evidence required to identify the designated zone. |
| OE-008 | Precision landing | Define the landing reference, landing-completion conditions and precision-landing acceptance criteria. |
| OE-009 | Landing-zone acquisition failure | Define the expected behavior when the designated landing zone cannot be acquired and whether clarification of mission scope is needed before deriving a requirement. No response behavior is selected here. |
| OE-010 | GNSS degradation | Define which GNSS information conditions constitute degradation and how they are distinguished from nominal availability and loss. |
| OE-011 | GNSS loss | Define which GNSS availability conditions constitute loss. |
| OE-012 | GNSS detection performance | Define detection-performance acceptance criteria, including timeliness, missed detections and false detections under nominal, degraded and lost-GNSS test conditions. |
| OE-013 | Degraded navigation | Define the alternative-information availability assumptions, applicable operating conditions and degraded position/motion estimation-performance criteria, including GNSS-unavailable operation. |
| OE-014 | Mission continuation | Define the navigation-information and system-capability criteria permitting continuation, including how continued eligibility is assessed as conditions change. |
| OE-015 | Safe termination | Define the termination behavior, safe terminal state, completion evidence and feasibility under the remaining navigation capability. |
| OE-016 | Supervisor intervention | Define permitted supervisory directions, required responses and precedence relative to autonomous decisions; distinguish effects on DAWN from termination of the external simulation or test. |
| OE-017 | Mission information | Define the mission information needed to interpret the waypoint route and designated landing objective without allocating its source or implementation. |
| OE-018 | Mission status | Define the status information needed for mission supervision and its availability criteria without choosing a communication implementation. |
| OE-019 | Authorization boundary | Define which preparatory activities may precede authorization and the point at which authorized autonomous mission execution begins. |
| OE-020 | Test operating conditions | Define the test environment, initial conditions and operating limits applicable to nominal and GNSS-degraded scenarios. Mission assumptions remain test preconditions. |
| OE-021 | Mission outcome evidence | Define evidence and acceptance rules distinguishing nominal completion, degraded continuation, degraded completion and autonomous safe termination. Supervisor intervention or test termination alone is not evidence of autonomous resilience success. |
