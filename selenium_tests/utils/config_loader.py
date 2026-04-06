import os
import json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


#__file__ = C:\Users\Anas\documents\saucedemo_qa\selenium_tests\utils\config_loader.py
# dirname once =saucedemo_qa\selenium_tests\utils\
# dirname twice = saucedemo_qa\selenium_tests\
# dirname three times = saucedemo_qa\  this is where data/ lives

with open(os.path.join(BASE_DIR, "data", "config.json")) as f:
    config = json.load(f)
