"""
AINL3001 Knowledge-Driven AI
Equipment Troubleshooting Expert System

Backward Chaining

Backward chaining starts from a GOAL, such as a possible diagnosis
(for example "faulty_charger"), and works backwards through the rules
to find out what would need to be true.

When it reaches a symptom that only the user knows about, it asks
the user a yes/no question.

It only asks questions that matter for the goal, and it never asks
the same question twice.
"""


# --------------------------------------------------
# BACKWARD CHAINING
# --------------------------------------------------

def backward_chain(goal, kb, answers, ask):
    """
    Return True if goal can be proved, False if not.

    goal    : the fact we want to prove, e.g. "faulty_charger"
    kb      : the knowledge base loaded from data/rules.json
    answers : the answers the user has given so far,
              e.g. {"wont_turn_on": True}
    ask     : a function that asks the user a question
              and returns True (yes) or False (no)
    """

    # Case 1: the goal is a symptom only the user can tell us about

    if goal in kb["questions"]:

        if goal not in answers:

            question = kb["questions"][goal]["text"]

            answers[goal] = ask(goal, question)

        return answers[goal]

    # Case 2: the goal is the conclusion of one or more rules

    for rule in kb["rules"]:

        if rule["then"] == goal:

            rule_works = True

            for condition in rule["if"]:

                if not backward_chain(condition, kb, answers, ask):

                    rule_works = False

                    break

            if rule_works:
                return True

    return False



# --------------------------------------------------
# TESTING AREA
# --------------------------------------------------

def pretend_user(fact, question):
    """
    Pretend to be a user whose charger is faulty,
    so the code can be tested without typing answers.
    Any question not listed here is answered "no".
    """

    yes_answers = [
        "wont_turn_on",
        "charger_plugged_in",
        "charging_light_off",
        "socket_works_for_other_devices",
    ]

    answer = fact in yes_answers

    print(question, "->", answer)

    return answer


if __name__ == "__main__":

    import json

    with open("data/rules.json") as file:
        kb = json.load(file)

    answers = {}

    print("Goal: faulty_charger\n")

    result = backward_chain("faulty_charger", kb, answers, pretend_user)

    print("\nProved?", result)
    print("Questions asked so far:", len(answers))

    print("\nGoal: flat_battery\n")

    result = backward_chain("flat_battery", kb, answers, pretend_user)

    print("\nProved?", result)
    print("Questions asked so far:", len(answers))


