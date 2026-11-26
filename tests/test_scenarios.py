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

    # Network
    ("network", ["no_wifi_networks_shown", "airplane_mode_on",
                 "other_devices_work_on_wifi"], "wifi_turned_off"),
    ("network", ["no_wifi_networks_shown", "other_devices_work_on_wifi",
                 "still_no_networks_after_restart"], "faulty_wifi_adapter"),
    ("network", ["connected_but_no_internet", "other_devices_also_offline"],
     "router_or_broadband_fault"),
    ("network", ["connected_but_no_internet", "other_devices_work_on_wifi"],
     "laptop_network_settings_fault"),
    ("network", ["connection_keeps_dropping", "far_from_router"], "weak_wifi_signal"),

    # Sound, keyboard and touchpad
    ("audio_input", ["some_keys_not_working", "crumbs_or_dust_under_keys"], "dirty_keyboard"),
    ("audio_input", ["whole_keyboard_dead", "usb_keyboard_works"], "keyboard_ribbon_cable_fault"),
    ("audio_input", ["touchpad_not_responding", "touchpad_off_light_on",
                     "usb_mouse_works"], "touchpad_turned_off"),
    ("audio_input", ["touchpad_not_responding", "touchpad_dead_after_restart",
                     "usb_mouse_works"], "touchpad_hardware_fault"),
    ("audio_input", ["some_keys_not_working", "liquid_spilled"], "water_damage"),


    # Performance
    ("performance", ["fan_loud_all_the_time", "laptop_hot_underneath",
                     "dust_in_vents"], "blocked_cooling"),
    ("performance", ["laptop_runs_slowly", "many_programs_at_startup"],
     "too_many_startup_programs"),

    # Storage
    ("storage", ["laptop_runs_slowly", "storage_almost_full"], "storage_full"),
    ("storage", ["clicking_noise", "files_corrupted"], "failing_drive"),
    ("storage", ["wont_load_system", "started_after_update"], "broken_system_update"),

    # A user who says NO to everything should get no diagnosis
    ("power", [], None),

]


def run_scenario(area, yes_facts):
    # A pretend user who says YES only to the facts in yes_facts.
    def pretend_user(fact, question):
        return fact in yes_facts

    return diagnose(area, kb, pretend_user)