"""
AINL3001 Knowledge-Driven AI
Equipment Troubleshooting Expert System

Scenario Tests

Each scenario is a pretend user with a known problem.
We run the whole expert system and check it finds the right diagnosis.
This also measures accuracy and the average number of questions asked.

Run with:

    python3 -m pytest -v            (the tests)
    python3 -m tests.test_scenarios (a summary table for the report)
"""

from src.knowledge_base import load_knowledge_base
from src.expert_system import diagnose

kb = load_knowledge_base()


# --------------------------------------------------
# PART 1: THE SCENARIOS
# --------------------------------------------------

# Each scenario: (problem area, facts the user says YES to, expected diagnosis)

scenarios = [
    # Power
    ("power", ["wont_turn_on", "on_battery_only"], "flat_battery"),
    ("power", ["wont_turn_on", "charger_plugged_in", "charging_light_off",
               "socket_works_for_other_devices"], "faulty_charger"),
    ("power", ["battery_drains_fast", "laptop_over_3_years_old"], "worn_out_battery"),
    ("power", ["battery_swollen"], "swollen_battery"),

    # Display
    ("display", ["wont_turn_on", "charger_plugged_in", "lights_or_fan_on",
                 "external_monitor_shows_picture"], "faulty_screen"),
    ("display", ["screen_cracked"], "damaged_screen_panel"),
    ("display", ["screen_flickers", "flicker_worse_when_lid_moves",
                 "external_monitor_shows_picture"], "loose_display_cable"),
    ("display", ["screen_very_dim", "faint_image_with_torch"], "failed_backlight"),

]


def run_scenario(area, yes_facts):
    # A pretend user who says YES only to the facts in yes_facts.
    def pretend_user(fact, question):
        return fact in yes_facts

    return diagnose(area, kb, pretend_user)