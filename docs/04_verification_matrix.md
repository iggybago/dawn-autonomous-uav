# DAWN Verification Strategy and Requirements Verification Matrix

## 1. Purpose and Scope

This document defines the initial verification strategy and primary verification
cases for the 27 current DAWN requirements. Its authoritative sources are:

- [Mission Concept](01_mission_concept.md): intended mission, success criteria,
  assumptions and exclusions.
- [System Requirements](02_system_requirements.md): authoritative requirements,
  proposed methods and Open Engineering Decisions.
- [System Architecture](03_system_architecture.md): functional responsibilities,
  interfaces, response chains and information boundaries.

**Verification** demonstrates that specified requirements are satisfied.
**Validation** demonstrates that the resulting system is suitable for the
intended mission described by the Mission Concept. Requirement-level evidence
can support validation, but mission suitability also depends on the relevance
of the requirements, scenarios and operating assumptions.

This is a planning document. It contains no execution results and claims neither
completed verification nor completed validation. Requirements remain Draft;
case readiness is separate from requirement status and implementation readiness.

The baseline is simulation-first. Fault injection is limited to the defined
GNSS degradation/loss scenario. Other sensor, motor, battery and multiple-fault
verification are outside this baseline. Mission assumptions remain test
preconditions and Mission Concept exclusions continue to apply. No algorithms,
implementation technologies, hardware or quantitative thresholds are selected.

## 2. Verification Methods

| Method | Meaning and intended use |
| --- | --- |
| Inspection | Examine documents, interface definitions, configuration or implementation artifacts for specified properties and traceability without exercising the behavior. |
| Analysis | Evaluate mathematical relationships or recorded numerical evidence against specified criteria, including performance metrics and feasibility arguments. |
| Simulation | Execute the modeled vehicle/system in a defined simulated environment and evaluate its dynamic behavior against the requirement. |
| Test | Apply controlled inputs or conditions to a function, interface or system and compare observable responses with defined expected behavior. |
| Demonstration | Observe execution of a capability under defined conditions. Qualitative observation alone is insufficient for requirements with numerical performance criteria. |
| Fault Injection Test | Deliberately modify simulated GNSS information or availability under controlled conditions and evaluate detection, degraded operation or termination behavior. Simulation provides the execution environment. |

The **primary method** is the principal approach assigned to each requirement.
**Secondary methods** provide complementary evidence or isolate contributing
behavior; they do not create additional primary cases or replace the evidence
needed by the primary method. Section 9 identifies useful secondary methods.
Inspection, Analysis and Demonstration are defined here even though none is
assigned as a primary method in the current matrix.

## 3. Case Readiness and Engineering Dependencies

Every current case has **Readiness = Partially Defined**. This means a meaningful
verification concept is identifiable, but final executable pass/fail criteria
depend on unresolved engineering decisions. A case definition is not an
execution result. None of the cases is marked Verified, Passed or Failed.

The matrix lists principal dependencies from the existing
[Open Engineering Decisions](02_system_requirements.md#open-engineering-decisions).
These lists are not a waiver of inherited or scenario-dependent criteria:

- OE-020 applies to applicable simulated environments, initial conditions and
  operating limits.
- OE-021 applies where mission continuation, mission completion and safe
  termination outcomes must be distinguished.
- Parent and referenced-requirement dependencies continue to apply.
- Mission-level cases inherit applicable readiness, navigation, flight,
  acquisition and landing criteria needed for the claimed outcome.

Final procedures must define the applicable stimuli, initial conditions,
observation intervals, metrics, numerical tolerances, expected behavior and
required scenario coverage. Repetition counts, statistical treatment and
sampling adequacy must follow the resolved criteria; none is invented here.
Negative claims, such as no unauthorized start or no premature phase transition,
need defined observation intervals and sufficient event coverage.

A case may contain multiple scenarios and repetitions under its single primary
identifier. One run may contribute evidence to several cases, but each case
requires its own traceable evaluation. Component evidence does not by itself
establish an end-to-end mission outcome.

## 4. Primary Requirements Verification Matrix

Each requirement has exactly one primary case named `VC-<REQUIREMENT-ID>`.
The allocation matches the methods proposed in the System Requirements:
**10 Simulation, 9 Test and 8 Fault Injection Test**.

### 4.1 Mission

| Requirement ID | Verification Case ID | Primary method | Verification objective | Required objective evidence | Principal OE dependencies | Readiness |
| --- | --- | --- | --- | --- | --- | --- |
| MIS-001 | VC-MIS-001 | Simulation | Autonomously complete the nominal mission sequence, maintain controlled flight and land at the designated zone under nominal conditions. | Mission definition; mission-state transition logs; state and trajectory histories; landing measurements; intervention record; independently evaluated mission outcome. | OE-003, OE-020, OE-021; applicable constituent criteria, particularly OE-002, OE-004, OE-005, OE-007 and OE-008. | Partially Defined |
| MIS-002 | VC-MIS-002 | Fault Injection Test | Continue actual mission execution after controlled GNSS degradation/loss when continuation criteria are satisfied; a mode change alone is insufficient. | Injection/detection timeline; alternative-information availability; estimate validity; assessment and decision records; post-fault progress and trajectory; outcome record. | OE-013, OE-014, OE-020, OE-021; supporting detection and transition criteria under OE-010, OE-011, OE-012 and OE-003. | Partially Defined |
| MIS-003 | VC-MIS-003 | Fault Injection Test | Autonomously reach the defined safe terminal state when continued operation becomes inappropriate after GNSS degradation/loss. | Complete detection-to-response timeline; cancellation events; guidance references; actuator commands; physical state histories; operational completion evidence; independent terminal-state evaluation. | OE-014, OE-015, OE-020, OE-021; OE-004 for applicable stability criteria. | Partially Defined |

MIS-002 establishes conditional continuation. Successful degraded completion
requires completion of the remaining mission, including designated-zone landing,
as specified by Mission Concept §6. Record continuation and eventual outcome
separately. Safe termination demonstrates resilience without constituting
completion of the planned mission.

### 4.2 System

| Requirement ID | Verification Case ID | Primary method | Verification objective | Required objective evidence | Principal OE dependencies | Readiness |
| --- | --- | --- | --- | --- | --- | --- |
| SYS-001 | VC-SYS-001 | Test | Accept the mission information needed for the ordered waypoint route and designated landing objective. | Submitted mission information; acceptance result; observable accepted route and landing designation compared with the supplied information. | OE-017. | Partially Defined |
| SYS-002 | VC-SYS-002 | Test | Establish the defined initialized state before pre-flight checks commence; exercise complete and incomplete initialization conditions. | Local initialization evidence; initialized-state observations; initialization-completion and pre-flight-start events. | OE-001; OE-003 for transition semantics. | Partially Defined |
| SYS-003 | VC-SYS-003 | Test | Evaluate the defined pre-flight checks and produce the correct readiness result for ready and not-ready conditions. | Controlled check inputs; individual check outcomes; consolidated readiness result; comparison with independently determined expected results. | OE-002. | Partially Defined |
| SYS-004 | VC-SYS-004 | Test | Make the required current mission status available to mission supervision across applicable phases and operating conditions. | Status observed at the supervisory interface; timestamps; comparison with actual mission state and events. | OE-018; OE-003 for phase/status semantics. | Partially Defined |

For SYS-004, an internal publication flag is insufficient without evidence of
availability at the defined supervisory interface.

### 4.3 Guidance, Navigation and Control

| Requirement ID | Verification Case ID | Primary method | Verification objective | Required objective evidence | Principal OE dependencies | Readiness |
| --- | --- | --- | --- | --- | --- | --- |
| GNC-001 | VC-GNC-001 | Simulation | Maintain the specified flight-stability criteria throughout applicable airborne scenarios and transitions. | Relevant attitude, angular-rate, position and velocity histories; references and commands; excursions and durations against defined limits; actuator-limit records. | OE-004, OE-020. | Partially Defined |
| GNC-002 | VC-GNC-002 | Simulation | Execute autonomous takeoff from the defined launch condition to the takeoff-completion condition. | Initial-state record; takeoff references; physical state/trajectory and actuator-command histories; completion event checked against physical evidence. | OE-003, OE-020; applicable OE-004 criteria. | Partially Defined |
| GNC-003 | VC-GNC-003 | Simulation | Navigate waypoints in their specified order while meeting tracking and waypoint-attainment criteria. | Waypoint list; active-objective history; reference and actual trajectories; tracking-error histories; acceptance events and corresponding vehicle states. | OE-005; OE-003 for progression semantics. | Partially Defined |
| GNC-004 | VC-GNC-004 | Simulation | Execute approach to the identified designated zone and reach the defined approach-completion condition. | Target identification and validity; approach-entry event; guidance references; trajectory relative to the zone; completion evidence. | OE-003, OE-020; OE-007 for valid identification and target information. | Partially Defined |
| GNC-005 | VC-GNC-005 | Simulation | Land at the designated zone within the precision and landing-completion criteria, including applicable degraded scenarios. | External landing reference; physical state/trajectory; perception outputs and validity; guidance/actuator histories; measured landing error and completion evidence. | OE-008; OE-007; OE-013 and OE-014 for degraded variants. | Partially Defined |

Evaluate physical tracking against external reference state. Agreement between
a command and an inaccurate onboard estimate cannot establish physical tracking
accuracy. GNC-005 retains nominal and degraded coverage consistent with its
parent requirements; Section 9 identifies supporting fault injection.

### 4.4 State Estimation / Navigation

| Requirement ID | Verification Case ID | Primary method | Verification objective | Required objective evidence | Principal OE dependencies | Readiness |
| --- | --- | --- | --- | --- | --- | --- |
| EST-001 | VC-EST-001 | Simulation | Estimate the required position and motion quantities from available navigation information within the defined performance criteria. | Consumed observations; time-aligned estimates and external reference states; validity histories; estimation-error histories and numerical metrics. | OE-006; OE-020 for operating conditions. | Partially Defined |
| EST-002 | VC-EST-002 | Fault Injection Test | Supply estimates meeting degraded-navigation criteria using alternative information, including intervals with GNSS entirely unavailable. | Actual injected-input history; GNSS availability; alternative-information provenance and availability; estimates and validity; reference states; error histories throughout the fault interval. | OE-013; OE-006 for quantities/conventions; OE-010 and OE-011 for fault definitions. | Partially Defined |

EST-002 has a meaningful verification concept, but executable scenarios depend
on the alternative-information source and availability assumptions under OE-013.
Landing-zone perception is not assumed to provide general GNSS-denied navigation.

### 4.5 Autonomous Mission Management

| Requirement ID | Verification Case ID | Primary method | Verification objective | Required objective evidence | Principal OE dependencies | Readiness |
| --- | --- | --- | --- | --- | --- | --- |
| AUT-001 | VC-AUT-001 | Test | Prevent autonomous mission commencement without authorization and establish that any commencement follows authorization. | Authorization receipt history; preparation events; mission-start events; defined observation interval with authorization absent. | OE-019; OE-003 for the execution-start boundary. | Partially Defined |
| AUT-002 | VC-AUT-002 | Test | Prevent takeoff when readiness does not permit it and release the readiness gate when permitted while respecting other prerequisites. | Readiness result; gate state; takeoff-objective/reference issuance; physical takeoff evidence where applicable. | OE-002; OE-003 for takeoff initiation. | Partially Defined |
| AUT-003 | VC-AUT-003 | Simulation | Progress through nominal phases in order, advancing only when the current completion criteria hold; include unsatisfied completion conditions. | Mission-state transitions; completion-condition evidence; active objectives; references before and after transitions. | OE-003; relevant phase criteria including OE-005, OE-007 and OE-008. | Partially Defined |
| AUT-004 | VC-AUT-004 | Fault Injection Test | After GNSS detection, correctly assess navigation information and system capability for conditions permitting and preventing continuation. | Authoritative detection event; exact assessment inputs and validity; capability records; assessment result and rationale; independent evaluation against defined criteria. | OE-014; OE-013; OE-010, OE-011 and OE-012 for the triggering fault/detection. | Partially Defined |
| AUT-005 | VC-AUT-005 | Test | Select continuation when the assessment permits it and safe termination otherwise, covering both branches. | Assessment-result inputs; corresponding Mission Management decision outputs; linkage to applicable assessment conditions. | OE-014, including inherited AUT-004 dependencies for representative assessment conditions. | Partially Defined |
| AUT-006 | VC-AUT-006 | Fault Injection Test | Following detection and continuation selection, enter the defined degraded operation and apply its required functional changes. | Injection/detection timeline; assessment/decision events; mode-transition history; navigation validity and affected execution-context outputs. | OE-003, OE-013; inherited OE-014. | Partially Defined |

AUT-005's isolated two-branch decision rule can be specified now. Its complete
requirement-level case remains Partially Defined because assessment conditions
and inherited dependencies remain unresolved. Authorization and readiness are
necessary conditions; neither alone requires immediate mission commencement
or takeoff.

### 4.6 Perception

| Requirement ID | Verification Case ID | Primary method | Verification objective | Required objective evidence | Principal OE dependencies | Readiness |
| --- | --- | --- | --- | --- | --- | --- |
| PER-001 | VC-PER-001 | Simulation | Perform autonomous search for the designated zone during acquisition within defined search conditions, coordinating any required search motion. | Acquisition request/status; observation histories; search activity and results; motion objectives/trajectory where applicable; external scene definition. | OE-007, OE-020. OE-009 governs any proposed acquisition-failure response extension. | Partially Defined |
| PER-002 | VC-PER-002 | Simulation | Identify the designated zone according to identification criteria before approach begins; inhibit approach while identification is unsatisfied. | Designation and observations; perception identification/target outputs and validity; external reference identity; identification and approach timestamps; negative controls. | OE-007; OE-003 for approach entry. | Partially Defined |

Search activity, identification correctness and approach gating need distinct
evidence. Expected search outcomes depend on OE-007. No acquisition-failure
response is selected or added to the baseline here; that scope remains OE-009.

### 4.7 Safety / Resilience

| Requirement ID | Verification Case ID | Primary method | Verification objective | Required objective evidence | Principal OE dependencies | Readiness |
| --- | --- | --- | --- | --- | --- | --- |
| SAF-001 | VC-SAF-001 | Fault Injection Test | Detect defined GNSS degradation within detection-performance criteria, including nominal controls for false declarations. | Injected degradation profile; actual degradation-onset reference; observations/quality consumed by DAWN; authoritative Health/FDIR declarations; delays, misses and false declarations. | OE-010, OE-012; OE-011 for distinguishing loss. | Partially Defined |
| SAF-002 | VC-SAF-002 | Fault Injection Test | Detect defined GNSS loss within performance criteria and distinguish it from permitted nominal availability behavior. | GNSS delivery/availability timeline; loss-onset reference; Health/FDIR declarations; detection delays, misses and false declarations. | OE-011, OE-012; OE-010 for condition classification. | Partially Defined |
| SAF-003 | VC-SAF-003 | Fault Injection Test | Following termination selection, execute the predefined behavior through Guidance, Control and Vehicle functions. | Selection event; termination objectives/references; actuator histories; physical state histories; execution milestones and operational completion evidence. | OE-015; OE-003; inherited OE-014, OE-020 and OE-021. | Partially Defined |
| SAF-004 | VC-SAF-004 | Test | Cease planned mission pursuit on termination selection, cancel affected objectives and supersede their references. | Selection/cancellation events; active-objective ownership; waypoint/acquisition progression; reference histories showing the termination execution context. | OE-003, OE-015; inherited OE-014. | Partially Defined |
| SAF-005 | VC-SAF-005 | Test | Respond correctly to each permitted supervisory direction and apply defined precedence relative to autonomous decisions. | Direction issuance/receipt; mission state; competing decision where applicable; resulting commands/status/behavior; separate external test-stop record. | OE-016. | Partially Defined |

For SAF-004, motion temporarily aligned with an old route is not sufficient to
infer continued mission pursuit. Evidence must establish which objective owns
the commands and whether superseded objectives remain active.

## 5. Evidence and Observability

The architecture's FI-22 interface provides external validation outputs.
Instrumentation must record the responsible functions' actual inputs, outputs
and events without taking over their autonomous responsibilities. State Estimation
produces estimates and diagnostics; Health/FDIR declares the GNSS condition;
Mission Management assesses continuation and selects the response; Guidance,
Control and Vehicle functions execute it.

| Evidence category | Expected records and purpose |
| --- | --- |
| Identification and configuration | Verification case/scenario identification; source, model and configuration/version information; mission definition; random seeds where applicable. |
| Initial conditions | Initial vehicle state, information availability, defined environment and operating assumptions under OE-020. |
| Time | Timestamps and a common time reference for observations, state samples, commands and events; timing resolution adequate for the eventual criteria. |
| Fault stimulus | Fault-injection command, requested profile and actual fault effect at the simulated navigation-information boundary. Record both times; command time is not automatically degradation/loss onset. |
| Navigation observations | Information actually consumed by DAWN, with source/provenance, quality, availability and freshness. |
| Estimated and reference state | Estimated state and validity; separately identified external reference state; time-aligned estimation-error histories and applicable metrics. |
| Health and assessment | Authoritative Health/FDIR declarations; continuation-assessment inputs, their validity, capability information, result and rationale. |
| Mission decisions | Mission Management decisions; authorization receipt; initialization/readiness evidence; mission phase transitions and their completion-condition evidence. |
| Objectives | Active and cancelled objectives; cancellation/supersession events; objective ownership of subsequent references and commands. |
| Perception | Input designation and observation provenance; perception outputs, identification evidence, target geometry and validity; approach-entry time. |
| Guidance and actuation | Guidance references; actuator commands; applicable limits and execution-capability reports; resulting physical state histories and trajectory histories/plots. |
| Completion and outcome | Operational completion evidence available to DAWN; separately recorded independent external outcome evaluation; distinction between continuation, mission completion and safe termination. |
| Supervision and test ending | Supervisory intervention, direction receipt and resulting DAWN response; external test-stop reason and time, recorded separately. |
| Physical metadata | Units, coordinate frames, time references and validity metadata where applicable; source and destination frames and conventions for any transformation. |
| Evidence integrity | Missing-record detection, sampling adequacy, retained raw numerical data, traceability to metric calculations and reproducibility information. |

Use SI units, NED navigation axes (North, East, Down) and FRD body axes (Forward,
Right, Down), unless an interface explicitly documents otherwise. Any rotation
or quaternion convention used must be explicit. Stale/missing-data behavior and
validity semantics must be specified consistently with the architecture.

Plots summarize behavior; retain the numerical histories and calculations from
which they are derived. Independent outcome evaluation must compare physical
behavior with defined criteria rather than accepting an internal completion
flag as sufficient evidence. Mission-status availability must be observed at
the supervisory interface, not inferred solely from an internal production event.

## 6. Ground-Truth Separation and Instrumentation Boundaries

External simulation ground truth may be used to:

- Generate defined simulated observations through the specified observation
  interfaces and applicable observation/error/availability assumptions.
- Serve as independent verification reference data for state, detection,
  identification, trajectory, landing and mission-outcome evaluation.

It shall not be used directly by autonomous DAWN functions as onboard navigation
state, fault truth, perception truth, decision input or a mission-completion
verdict. This restriction includes State Estimation, Health/FDIR, Perception,
Mission Management, Guidance and Control. Privileged truth or evaluator verdicts
must not be routed indirectly through another function into an autonomous
information or decision path.

Verification instrumentation must distinguish information available to DAWN at
decision time from privileged information available only to the external
evaluator. Evidence flows outward for evaluation; reference errors and external
outcome verdicts are not fed back to autonomous decisions or completion gates.
Defined mission information, including route and landing-zone designation,
remains legitimate input under SYS-001 and OE-017; designation must not be
confused with an externally supplied identification result.

Controlled component-test inputs may be supplied at documented component
boundaries to isolate a rule. Such evidence applies to that component behavior
and cannot replace integrated evidence that upstream functions actually produced
the inputs. Instrumentation must preserve the functional boundaries and must
not materially alter the behavior being evaluated.

## 7. GNSS Fault-Injection Strategy

GNSS degradation/loss verification requires controlled modification of simulated
navigation information or its availability. The injection definition must
identify the affected information, profile, onset and duration under the
applicable conditions, without expanding the baseline beyond the defined GNSS
scenario. Include nominal controls and relevant boundary conditions once
OE-010, OE-011 and OE-012 define degradation, loss and detection performance.

Directly forcing a Health/FDIR detection flag may be useful for an isolated
component test. It shall not count as evidence that GNSS degradation/loss
detection or end-to-end resilience has been verified. The integrated cases must
observe Health/FDIR declaring the condition from information available to DAWN,
then observe Mission Management and the execution functions responding.

Compare actual fault effect and the defined fault-onset reference with the
authoritative declaration timestamp. Detection-delay, missed-detection and
false-declaration evaluations remain subject to OE-012. Record navigation
validity and alternative-information availability throughout the fault interval
under OE-013. Continued eligibility must be assessed as defined under OE-014;
a single initial continuation decision does not establish indefinite capability.

## 8. Safe-Termination Verification

Safe-termination evidence must cover the complete functional chain:

1. Fault/health evidence, navigation validity and relevant capability evidence.
2. Mission Management continuation assessment and termination decision.
3. Cancellation/supersession of active mission objectives and references.
4. Guidance references for the predefined termination behavior.
5. Control tracking and actuator-command generation.
6. Vehicle execution and observable physical state histories.
7. Operational completion evidence and Mission Management outcome reporting.
8. Independent external evaluation against the defined behavior and terminal
   state.

AUT-005 decision selection, AUT-006 degraded transition, SAF-003 execution and
MIS-003 terminal outcome establish different facts. Component results support
but do not replace integrated outcome evidence. OE-015 must define the maneuver,
terminal state, completion evidence and feasibility under remaining navigation
capability. No maneuver, terminal state or surviving navigation capability is
assumed here.

Stopping the external simulator shall not constitute evidence of successful
safe termination. Selecting termination, issuing commands, receiving a supervisor
intervention or producing an internal completion flag is also insufficient by
itself. Record external test termination separately under OE-016. If a run ends
before the required terminal-state evidence is obtained, it cannot establish
the autonomous termination outcome. Distinguish safe termination from planned
mission completion under OE-021.

## 9. Supporting / Secondary Verification Methods

These activities support the existing primary cases. They create no additional
requirement IDs or verification-case IDs and make no verification-result claim.

| Applicable requirements | Secondary method and purpose |
| --- | --- |
| GNC-001 through GNC-005; EST-001 and EST-002 | Analysis of retained numerical histories against the specified performance metrics, conventions and tolerances. |
| SAF-001 and SAF-002 | Analysis of detection latency, misses and false declarations across the defined scenarios and repetitions. |
| AUT-003 | Test individual transition gates with satisfied and unsatisfied completion conditions alongside integrated Simulation. |
| AUT-004 through AUT-006 | Isolated Test of assessment/decision/transition logic; integrated Fault Injection Test to establish the detection-to-response chain. |
| PER-002 | Test the identification-to-approach gate separately from simulated identification performance. |
| GNC-005 | Fault Injection Test for landing under applicable GNSS-degraded conditions alongside nominal Simulation. |
| MIS-003 and SAF-003 | Analysis of safe-termination feasibility under remaining navigation and execution capability, supporting the dynamic execution evidence. |
| SAF-004 and SAF-005 | Simulation to establish that cancellation or supervisory direction affects physical execution beyond an internal state change. |
| SYS-001 and SYS-004 | Inspection of mission-information and status-interface definitions and traceability, supporting behavioral Test. |

## 10. Architecture-Derived Verification Needs

The following are **candidate verification needs**, not existing requirements,
not additional current verification cases and not current acceptance criteria.
They require an agreed requirement basis or interface definition before they
can become baseline acceptance obligations. References identify related existing
engineering decisions without treating those decisions as resolved.

| Candidate need | Future definition or evaluation needed |
| --- | --- |
| Ground-truth isolation | Inspect information paths and evaluate access to privileged reference data so neither direct nor indirect truth/verdict inputs can affect autonomous decisions; related to OE-017 and OE-020/OE-021. |
| Decision-authority separation | Establish that Estimation supplies diagnostics, Health/FDIR declares GNSS condition, Mission Management decides continuation/termination and execution functions implement the response; related to OE-010 through OE-015. |
| Validity propagation | Specify and evaluate consumer behavior for stale, missing or invalid state and target information; related to OE-006, OE-007, OE-013 and OE-014. |
| Coordinated mode transitions | Establish consistent operating context and cancellation/supersession across affected functions; related to OE-003, OE-014 and OE-015. |
| Response timing | Distinguish onset, detection, assessment, decision, reference replacement and physical response; derive timing criteria where needed under OE-003, OE-012, OE-014 and OE-015. |
| Reference feasibility | Establish how Guidance and Control expose inability to execute references within remaining capability; related to OE-004, OE-013, OE-014 and OE-015. |
| Simulation credibility | Establish that modeled dynamics, observations, fault effects and numerical/time resolution support the claimed evidence under OE-020. |
| Evidence integrity | Define sufficient recording coverage, time alignment, provenance and reproducible external evaluation without materially changing autonomous behavior; related to OE-020 and OE-021. |
| Continued-eligibility reassessment | Exercise changing continuation conditions, rather than only the first post-detection decision, once OE-014 defines the applicable behavior. |
| Landing-zone acquisition failure handling | Clarify scope and expected response under OE-009 before deriving any acquisition-failure acceptance obligation; no alternate-site or termination behavior is selected. |
