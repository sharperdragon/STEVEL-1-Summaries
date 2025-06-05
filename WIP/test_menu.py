# test_menu.py
from menu_builder import build_complete_menu
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from WIP.menu_builder import build_complete_menu
# Sample top-level buttons
buttons = [
    ("Shuffle Rows", "shuffle-btn"),
    ("Reset Table", "reset-btn")
]

# Sample submenu
submenus = [
    {
        "label": "Hide Columns",
        "buttons": {
            "hide-col-1": "Column 1",
            "hide-col-2": "Column 2",
            "hide-col-3": "Column 3"
        }
    }
]

# Build the menu HTML
menu_html = build_complete_menu("test-tools", "🧪 Test Tools", buttons, submenus)

# Print to terminal
print(menu_html)

# Optionally write to a file
import os
desktop_path = os.path.expanduser("~/Desktop/test_menu_output.html")
with open(desktop_path, "w") as f:
    f.write(menu_html)