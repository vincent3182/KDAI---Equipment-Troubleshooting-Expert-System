"""
AINL3001 Knowledge-Driven AI
Equipment Troubleshooting Expert System

Explanation

Turns the list of rules that fired into plain English,
so the user can see WHY the system reached its answer.
"""


# --------------------------------------------------
# PART 1: DESCRIBING ONE FACT
# --------------------------------------------------

def describe_fact(fact, kb):
    # If the fact was a question, say what the user answered.
    if fact in kb["questions"]:
        return 'You said YES to "' + kb["questions"][fact]["text"] + '"'

    # If the fact is a diagnosis, use its cause sentence.
    if fact in kb["diagnoses"]:
        return kb["diagnoses"][fact]["cause"]

    # Otherwise just turn "no_power_reaching_laptop"
    # into "no power reaching laptop".
    return fact.replace("_", " ")



# --------------------------------------------------
# PART 2: EXPLAINING ONE RULE
# --------------------------------------------------

def explain_rule(rule, kb):
    reasons = []
    for condition in rule["if"]:
        reasons.append(describe_fact(condition, kb))

    sentence = "Rule " + rule["id"] + ": because\n"
    for reason in reasons:
        sentence = sentence + "   - " + reason + "\n"
    sentence = sentence + "   so we concluded: " + describe_fact(rule["then"], kb)
    return sentence