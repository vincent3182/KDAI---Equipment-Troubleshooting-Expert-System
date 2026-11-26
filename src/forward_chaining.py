"""
AINL3001 Knowledge-Driven AI
Equipment Troubleshooting Expert System

Forward Chaining

Forward chaining starts from the facts we know (the user's "yes"
answers) and keeps applying rules until nothing new can be added.

It also records which rules fired, in order, so the system can
explain how it reached each conclusion.
"""


# --------------------------------------------------
# FORWARD CHAINING
# --------------------------------------------------

def forward_chain(facts, rules):
    """
    Return (inferred_facts, fired_rules).

    facts : a set of known fact names, e.g. {"wont_turn_on"}
    rules : the list of rules, kb["rules"]

    inferred_facts : a NEW set with the original and inferred facts
    fired_rules    : rule IDs in the order they fired, e.g. ["P5", "P6"]
    """

    inferred_facts = set(facts)   # copy, so the input set is not changed
    fired_rules = []

    keep_going = True

    while keep_going:

        keep_going = False

        for rule in rules:

            all_known = True

            for condition in rule["if"]:
                if condition not in inferred_facts:
                    all_known = False

            if all_known and rule["then"] not in inferred_facts:
                inferred_facts.add(rule["then"])
                fired_rules.append(rule["id"])
                keep_going = True

    return inferred_facts, fired_rules

# --------------------------------------------------
# FIND DIAGNOSES
# --------------------------------------------------

def find_diagnoses(inferred_facts, kb):
    """
    Return the diagnosis names present in inferred_facts,
    sorted by priority, highest first.
    """

    found = []

    for priority in [5, 4, 3, 2, 1]:
        for diagnosis in kb["diagnoses"]:
            if diagnosis in inferred_facts:
                if kb["diagnoses"][diagnosis]["priority"] == priority:
                    found.append(diagnosis)

    return found

# --------------------------------------------------
# FIND RECOMMENDATIONS
# --------------------------------------------------

def find_recommendations(inferred_facts, kb):
    """
    Return the recommendation names present in inferred_facts.
    """

    found = []

    for recommendation in kb["recommendations"]:
        if recommendation in inferred_facts:
            found.append(recommendation)

    return found

# --------------------------------------------------
# EVIDENCE STRENGTH
# --------------------------------------------------

def evidence_strength(fact, fired_rules, kb):
    """
    Return how strong the evidence for a fact is:
    the number of conditions in the fired rule that concluded it.
    If several fired rules concluded it, use the largest.
    A fact that no fired rule concluded has strength 0.
    """

    strength = 0

    for rule in kb["rules"]:
        if rule["id"] in fired_rules and rule["then"] == fact:
            if len(rule["if"]) > strength:
                strength = len(rule["if"])

    return strength