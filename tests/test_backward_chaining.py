"""
AINL3001 Knowledge-Driven AI
Equipment Troubleshooting Expert System

Tests for Backward Chaining

These tests use a small, made-up knowledge base, so we know exactly
which questions should be asked and what the answers should be.

Run all tests from the main project folder with:

    python3 -m pytest
"""

from src.backward_chaining import backward_chain


# --------------------------------------------------
# A SMALL KNOWLEDGE BASE FOR TESTING
# --------------------------------------------------

kb = {
    "questions": {
        "rainy": {"area": "test", "text": "Is it raining?"},
        "cold": {"area": "test", "text": "Is it cold?"},
        "windy": {"area": "test", "text": "Is it windy?"},
    },
    "rules": [
        {"id": "T1", "if": ["rainy"], "then": "take_umbrella"},
        {"id": "T2", "if": ["take_umbrella"], "then": "stay_dry"},
        {"id": "T3", "if": ["rainy", "cold"], "then": "wear_coat"},
        {"id": "T4", "if": ["windy"], "then": "wear_coat"},
    ],
}


# --------------------------------------------------
# PRETEND USERS
# --------------------------------------------------

# Every question a pretend user is asked gets added to this list,
# so the tests can check how many times each question was asked.
questions_asked = []


def user_says_yes_to_rainy(fact, question):
    questions_asked.append(fact)
    return fact == "rainy"


def user_says_yes_to_windy(fact, question):
    questions_asked.append(fact)
    return fact == "windy"


def user_says_no_to_everything(fact, question):
    questions_asked.append(fact)
    return False


# --------------------------------------------------
# TESTS: ASKING QUESTIONS
# --------------------------------------------------

def test_question_is_asked_and_answer_is_saved():
    questions_asked.clear()
    answers = {}

    result = backward_chain("rainy", kb, answers, user_says_yes_to_rainy)

    assert result == True
    assert answers == {"rainy": True}


def test_same_question_is_never_asked_twice():
    questions_asked.clear()
    answers = {}

    # Both goals need "rainy", but it should only be asked once.
    backward_chain("take_umbrella", kb, answers, user_says_yes_to_rainy)
    backward_chain("stay_dry", kb, answers, user_says_yes_to_rainy)

    assert questions_asked.count("rainy") == 1



# --------------------------------------------------
# TESTS: FOLLOWING THE RULES
# --------------------------------------------------

def test_chained_rules_are_followed():
    questions_asked.clear()
    answers = {}

    # stay_dry needs take_umbrella, which needs rainy.
    result = backward_chain("stay_dry", kb, answers, user_says_yes_to_rainy)

    assert result == True


def test_goal_fails_when_a_condition_is_no():
    questions_asked.clear()
    answers = {}

    result = backward_chain("stay_dry", kb, answers, user_says_no_to_everything)

    assert result == False


def test_second_rule_is_tried_if_first_rule_fails():
    questions_asked.clear()
    answers = {}

    # T3 fails because it is not rainy, so T4 (windy) is tried instead.
    result = backward_chain("wear_coat", kb, answers, user_says_yes_to_windy)

    assert result == True