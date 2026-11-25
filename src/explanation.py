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



# --------------------------------------------------
# PART 3: EXPLAINING THE WHOLE ANSWER
# --------------------------------------------------

def explain(fired_rules, kb):
    if len(fired_rules) == 0:
        return "No rules fired, so there is nothing to explain."

    text = "How I reached this answer:\n"
    step = 1
    for rule in fired_rules:
        text = text + "\nStep " + str(step) + ". " + explain_rule(rule, kb) + "\n"
        step = step + 1
    return text


# --------------------------------------------------
# TESTING AREA
# --------------------------------------------------

if __name__ == "__main__":
    from src.knowledge_base import load_knowledge_base

    kb = load_knowledge_base()

    # Pretend these two rules fired (P2 then P3).
    fired = [kb["rules"][1], kb["rules"][2]]

    print(explain(fired, kb))