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



# --------------------------------------------------
# PART 3: THE WHOLE PROCESS
# --------------------------------------------------

def diagnose(area, kb, ask):
    answers = ask_questions(area, kb, ask)
    inferred_facts, fired_rules, diagnoses = work_out_results(answers, kb)

    result = {
        "diagnosis": None,
        "cause": "No diagnosis could be found from your answers.",
        "recommendations": [],
        "explanation": explain(fired_rules, kb),
        "questions_asked": len(answers),
    }

    # Step 5: give the top diagnosis and what to do about it.
    if len(diagnoses) > 0:
        top = diagnoses[0]
        result["diagnosis"] = top
        result["cause"] = kb["diagnoses"][top]["cause"]
        result["recommendations"] = find_recommendations(inferred_facts, kb)

    return result


# --------------------------------------------------
# TESTING AREA
# --------------------------------------------------

if __name__ == "__main__":
    from src.knowledge_base import load_knowledge_base

    kb = load_knowledge_base()

    # A pretend user whose charger is broken.
    def pretend_user(fact, question):
        print("Asked:", question)
        return fact in ["wont_turn_on", "charger_plugged_in",
                        "charging_light_off", "socket_works_for_other_devices"]

    result = diagnose("power", kb, pretend_user)

    print()
    print("Diagnosis:", result["diagnosis"])
    print("Cause:", result["cause"])
    print("Recommendations:", result["recommendations"])
    print("Questions asked:", result["questions_asked"])
    print()
    print(result["explanation"])