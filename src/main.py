"""
AINL3001 Knowledge-Driven AI
Equipment Troubleshooting Expert System

Command-Line Interface

This is the part of the system the user sees. It lets the user pick
a problem area, asks them yes/no questions, and shows the results.

Run it from the main project folder with:

    python3 -m src.main
"""

from src.knowledge_base import load_knowledge_base
from src.expert_system import diagnose


# --------------------------------------------------
# CHOOSING A PROBLEM AREA
# --------------------------------------------------

def choose_area(kb):
    """
    Show the problem areas as a numbered list and return
    the area the user picks, e.g. "power".
    """

    area_names = list(kb["areas"].keys())

    print("What kind of problem are you having?\n")

    for number in range(len(area_names)):

        area = area_names[number]

        print(f"  {number + 1}. {kb['areas'][area]}")

    while True:

        choice = input("\nEnter a number: ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(area_names):
            return area_names[int(choice) - 1]

        print(f"Please enter a number from 1 to {len(area_names)}.")



# --------------------------------------------------
# ASKING THE USER A QUESTION
# --------------------------------------------------

def ask_user(fact, question):
    """
    Ask the user a yes/no question.
    Return True for yes and False for no.
    Keep asking until the user types y or n.
    """

    while True:

        reply = input(f"{question} (y/n): ").strip().lower()

        if reply in ["y", "yes"]:
            return True

        if reply in ["n", "no"]:
            return False

        print("Please type y or n.")

        



# --------------------------------------------------
# SHOWING THE RESULTS
# --------------------------------------------------

def show_result(result):
    print()
    print("=" * 50)
    print("RESULTS")
    print("=" * 50)

    if result["diagnosis"] is None:
        print("\n" + result["cause"])
    else:
        print("\nLikely cause:")
        print("  " + result["cause"])

        print("\nWhat to do:")
        for recommendation in result["recommendations"]:
            print("  - " + recommendation)

    for warning in result["warnings"]:
        print("\nNote: " + warning)

    print("\nQuestions asked: " + str(result["questions_asked"]))

    print()
    print(result["explanation"])


# --------------------------------------------------
# RUNNING THE PROGRAM
# --------------------------------------------------

if __name__ == "__main__":

    kb = load_knowledge_base()

    print("=" * 50)
    print("LAPTOP TROUBLESHOOTING EXPERT SYSTEM")
    print("=" * 50)
    print()

    area = choose_area(kb)
    print()

    result = diagnose(area, kb, ask_user)

    show_result(result)