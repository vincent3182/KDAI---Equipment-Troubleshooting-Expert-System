"""
Tests for src/forward_chaining.py

Each test gives forward chaining some "yes" answers,
then checks the result is what we expect.
"""

from src.knowledge_base import load_knowledge_base
from src.forward_chaining import (forward_chain, find_diagnoses,
                                  find_recommendations, resolve_conflicts)


# --------------------------------------------------
# FORWARD CHAINING
# --------------------------------------------------

def test_rules_fire_in_a_chain():
    kb = load_knowledge_base()
    answers = {"wont_turn_on", "charger_plugged_in", "lights_or_fan_on",
               "external_monitor_shows_picture", "laptop_over_5_years_old"}
    facts, fired = forward_chain(answers, kb["rules"])
    assert fired == ["P5", "P6", "R3", "R4"]


def test_rule_does_not_fire_if_a_condition_is_missing():
    kb = load_knowledge_base()
    answers = {"wont_turn_on"}          # P1 also needs on_battery_only
    facts, fired = forward_chain(answers, kb["rules"])
    assert "flat_battery" not in facts


def test_original_answers_are_not_changed():
    kb = load_knowledge_base()
    answers = {"wont_turn_on", "on_battery_only"}
    forward_chain(answers, kb["rules"])
    assert answers == {"wont_turn_on", "on_battery_only"}

# --------------------------------------------------
# DIAGNOSES AND RECOMMENDATIONS
# --------------------------------------------------

def test_most_urgent_diagnosis_comes_first():
    kb = load_knowledge_base()
    answers = {"wont_turn_on", "charger_plugged_in", "lights_or_fan_on",
               "external_monitor_shows_picture", "battery_swollen"}
    facts, fired = forward_chain(answers, kb["rules"])
    assert find_diagnoses(facts, kb) == ["swollen_battery", "faulty_screen"]


def test_recommendation_is_found():
    kb = load_knowledge_base()
    answers = {"wont_turn_on", "on_battery_only"}
    facts, fired = forward_chain(answers, kb["rules"])
    assert find_recommendations(facts, kb) == ["recommend_charge_battery"]

