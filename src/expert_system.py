"""
AINL3001 Knowledge-Driven AI
Equipment Troubleshooting Expert System

Expert System

Joins all the parts together into our 5-step process:

    1. The user picks a problem area            (main.py)
    2. Ask questions with backward chaining     (backward_chaining.py)
    3. Work out new facts with forward chaining (forward_chaining.py)
    4. Pick the diagnosis                       (forward_chaining.py)
    5. Give the recommendations and explanation (explanation.py)
"""

from src.backward_chaining import backward_chain
from src.forward_chaining import forward_chain, find_diagnoses
from src.explanation import explain


# --------------------------------------------------
# PART 1: ASKING THE QUESTIONS (STEP 2)
# --------------------------------------------------

def ask_questions(area, kb, ask):
    # The notebook of answers, shared by every diagnosis,
    # so the same question is never asked twice.
    answers = {}

    # Try to prove each diagnosis that belongs to this area.
    for diagnosis in kb["diagnoses"]:
        if area in kb["diagnoses"][diagnosis]["areas"]:
            backward_chain(diagnosis, kb, answers, ask)

    return answers


def yes_answers(answers):
    # Forward chaining only needs the facts the user said YES to.
    facts = set()
    for fact in answers:
        if answers[fact] == True:
            facts.add(fact)
    return facts



# --------------------------------------------------
# PART 2: WORKING OUT THE RESULTS (STEPS 3 AND 4)
# --------------------------------------------------

def find_recommendations(inferred_facts, kb):
    recommendations = []
    for recommendation in kb["recommendations"]:
        if recommendation in inferred_facts:
            recommendations.append(kb["recommendations"][recommendation])
    return recommendations


def work_out_results(answers, kb):
    facts = yes_answers(answers)

    # Step 3: forward chaining adds every fact that follows.
    inferred_facts, fired_rules = forward_chain(facts, kb["rules"])

    # Step 4: find the diagnoses, highest priority first.
    diagnoses = find_diagnoses(inferred_facts, kb)

    return inferred_facts, fired_rules, diagnoses