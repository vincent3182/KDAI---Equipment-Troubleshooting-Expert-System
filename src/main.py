"""
AINL3001 Knowledge-Driven AI
Equipment Troubleshooting Expert System

Command-Line Interface

This is the part of the system the user sees. It lets the user pick
a problem area, asks them yes/no questions, and shows the results.

Run it from the main project folder with:

    python3 -m src.main
"""

import json

from src.backward_chaining import backward_chain


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