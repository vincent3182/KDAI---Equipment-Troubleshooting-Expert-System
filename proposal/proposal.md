Project Proposal: Equipment Troubleshooting Expert System
1. Team Information
Group name: Knowledge Driven Assignment
Name	Student number	GitHub username
Vincent Mikalauskas	C24498082	Vincent3182
Laurentiu Codreanu	C24387041	LaurCD
Repository: https://github.com/vincent3182/KDAI---Equipment-Troubleshooting-Expert-System.git
2. Problem Description
When a laptop stops working properly, most users do not know where to start. Is the battery flat, is the charger faulty, is it a software problem? Many people either give up or pay for a repair that was not needed, even though many faults can be solved by following a few simple checks in the right order.
Our project is an expert system that acts like a help-desk technician. The user describes the problems (for example, "the laptop will not turn on" or "the Wi-Fi keeps disconnecting"), the system asks follow-up questions, and it then gives a likely diagnosis and a recommended fix, together with an explanation of the reasoning that led to it.
Scope. To keep the project achievable in the time available, we will focus on one type of equipment: laptops, covering four problem areas:
Power and battery (will not turn on, will not charge)
Display (black screen, flickering)
Network (no Wi-Fi, connection dropping)
Performance (running slowly, overheating)
We aim for around 30 to 40 rules. If time allows, we will add a second device, such as a printer, using the same engine.
3. Proposed AI Approach
The main technique is rule-based reasoning using propositional logic, building on the Week 7 lab.
Knowledge base: facts (observed symptoms, such as `no_power` or `power_light_off`) and IF-THEN rules (for example, IF `no_power` AND `power_light_off` AND `charger_connected` THEN `possible_faulty_charger`).
Forward chaining: starting from the symptoms the user has entered, the system applies the rules repeatedly until no new facts can be inferred, producing all diagnoses and recommendations that follow.
Backward chaining: starting from a possible fault (a goal), the system works backwards to find which conditions must be true. If a condition is unknown, it asks the user. This means only relevant questions are asked, which is how a real technician works. We will treat this as a goal-directed depth-first search through the rules.
Explanation: the system will record which rules fired, so it can tell the user why it reached a conclusion.
Following the AIMA approach used in the labs:
Element	In our system
State	The set of facts currently known about the laptop
Actions	Ask the user a question; apply a rule to infer a new fact
Goal	A diagnosis and recommendation is established, or no rule applies
Knowledge representation	Propositional facts and IF-THEN rules
Reasoning mechanism	Forward and backward chaining
We are aware of the limitations of this approach: rules are treated as always true, and a result of "not established" does not mean a fault is absent. We will make this clear in the system's output, for example by saying "likely cause" rather than "the cause".

4. System Design
Components:
Knowledge base (`data/`): the rules, stored separately from the code (for example, as JSON) so they can be extended without changing the engine.
Working memory (`src/`): the facts known so far, stored as a Python set.
Inference engine (`src/`): forward chaining and backward chaining.
User interface (`src/`): a simple command-line program that asks questions and shows the result.
Explanation module (`src/`): shows the chain of rules that led to each conclusion.
Tests (`tests/`): automated tests using known symptom combinations and their expected diagnoses.
5. Planned Contributions
Student	Primary responsibilities
Vincent Mikalauskas	Knowledge base design (researching faults and writing the rules), rule file format, forward chaining engine
Laurentiu Codreanu	Backward chaining and question-asking, command-line interface, explanation module
Both	Testing, README and documentation, report, presentation
We will both review each other's code, and we will commit work regularly with meaningful commit messages so that the Git history shows the development of the project.
Timeline:
Week	Goal
Week 10	Knowledge base for power and display faults; forward chaining working
Week 11	Backward chaining, interface, explanations; remaining problem areas
Week 12	Testing, documentation, presentation
