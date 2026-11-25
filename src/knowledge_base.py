"""
AINL3001 Knowledge-Driven AI
Equipment Troubleshooting Expert System

Knowledge Base

Loads the rules, questions, diagnoses and recommendations
from data/rules.json, and checks that they follow our naming rules.
"""

import json


# --------------------------------------------------
# LOAD THE KNOWLEDGE BASE
# --------------------------------------------------

def load_knowledge_base(path="data/rules.json"):
    """
    Read the JSON file and return it as a dictionary with the keys
    'areas', 'questions', 'rules', 'diagnoses', 'recommendations'.
    """

    with open(path, encoding="utf-8") as file:
        kb = json.load(file)

    return kb

#--------------------------------------------------
#Validata the Knowledge base
#--------------------------------------------------

def validate_knowledge_base(kb):
    """
    Check the naming rules for data/rules.json.
    Return a list of error messages (strings).
    An empty list means the knowledge base is valid.
    """

    errors = []

    # Step 1: collect every fact that some rule concludes

    conclusions = set()

    for rule in kb["rules"]:
        conclusions.add(rule["then"])

    # Check 1: rule IDs are unique

    seen_ids = set()

    for rule in kb["rules"]:
        if rule["id"] in seen_ids:
            errors.append("Rule ID " + rule["id"] + " is used more than once")
        seen_ids.add(rule["id"])

    # Check 2: every condition is a question or a rule conclusion

    for rule in kb["rules"]:
        for condition in rule["if"]:
            if condition not in kb["questions"] and condition not in conclusions:
                errors.append("Rule " + rule["id"] + " needs unknown fact: " + condition)

    # Check 3: no question is also concluded by a rule

    for question in kb["questions"]:
        if question in conclusions:
            errors.append("Question " + question + " is also concluded by a rule")

    # Check 4: every diagnosis and recommendation is reachable

    for diagnosis in kb["diagnoses"]:
        if diagnosis not in conclusions:
            errors.append("Diagnosis " + diagnosis + " is never concluded by a rule")

    for recommendation in kb["recommendations"]:
        if recommendation not in conclusions:
            errors.append("Recommendation " + recommendation + " is never concluded by a rule")

    # Check 5: every conflicts_with name exists

    for diagnosis in kb["diagnoses"]:
        for conflict in kb["diagnoses"][diagnosis]["conflicts_with"]:
            if conflict not in conclusions and conflict not in kb["diagnoses"]:
                errors.append("Diagnosis " + diagnosis + " conflicts with unknown fact: " + conflict)

    return errors