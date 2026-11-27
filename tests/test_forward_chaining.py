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


# --------------------------------------------------
# CONFLICT RESOLUTION
# --------------------------------------------------

def test_stronger_evidence_wins():
    kb = load_knowledge_base()
    answers = {"some_keys_not_working", "crumbs_or_dust_under_keys", "liquid_spilled"}
    facts, fired = forward_chain(answers, kb["rules"])
    kept, warnings = resolve_conflicts(find_diagnoses(facts, kb), facts, fired, kb)
    assert kept == ["water_damage"]
    assert len(warnings) == 1


def test_equal_evidence_keeps_both():
    kb = load_knowledge_base()
    answers = {"no_wifi_networks_shown", "other_devices_work_on_wifi",
               "airplane_mode_on", "still_no_networks_after_restart"}
    facts, fired = forward_chain(answers, kb["rules"])
    kept, warnings = resolve_conflicts(find_diagnoses(facts, kb), facts, fired, kb)
    assert kept == ["faulty_wifi_adapter", "wifi_turned_off"]
    assert len(warnings) == 1


def test_no_conflict_gives_no_warnings():
    kb = load_knowledge_base()
    answers = {"battery_swollen"}
    facts, fired = forward_chain(answers, kb["rules"])
    kept, warnings = resolve_conflicts(find_diagnoses(facts, kb), facts, fired, kb)
    assert kept == ["swollen_battery"]
    assert warnings == []