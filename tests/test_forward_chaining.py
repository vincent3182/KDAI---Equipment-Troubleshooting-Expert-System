"""
Tests for src/knowledge_base.py

Test 1 checks our real rules.json has no mistakes.
The other tests add ONE mistake on purpose, and check
that the validator spots it.
"""

from src.knowledge_base import load_knowledge_base, validate_knowledge_base


def test_real_rules_have_no_mistakes():
    kb = load_knowledge_base()
    errors = validate_knowledge_base(kb)
    assert errors == []


def test_spots_a_typo_in_a_rule():
    kb = load_knowledge_base()
    kb["rules"].append({"id": "X1", "if": ["wont_turn_onn"], "then": "flat_battery"})
    errors = validate_knowledge_base(kb)
    assert errors != []


def test_spots_a_repeated_rule_id():
    kb = load_knowledge_base()
    kb["rules"].append({"id": "P1", "if": ["wont_turn_on"], "then": "flat_battery"})
    errors = validate_knowledge_base(kb)
    assert errors != []


def test_spots_a_rule_that_concludes_a_question():
    kb = load_knowledge_base()
    kb["rules"].append({"id": "X1", "if": ["battery_swollen"], "then": "wont_turn_on"})
    errors = validate_knowledge_base(kb)
    assert errors != []


def test_spots_advice_that_no_rule_reaches():
    kb = load_knowledge_base()
    kb["recommendations"]["recommend_magic"] = "Wave a wand."
    errors = validate_knowledge_base(kb)
    assert errors != []


def test_spots_a_typo_in_a_conflict():
    kb = load_knowledge_base()
    kb["diagnoses"]["flat_battery"]["conflicts_with"] = ["laptop_has_powerr"]
    errors = validate_knowledge_base(kb)
    assert errors != []