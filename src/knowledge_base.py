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