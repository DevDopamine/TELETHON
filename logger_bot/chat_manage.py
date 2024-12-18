import os
import json

allowed_file = "allowed_groups.json"

def load_allowed_groups():
    if os.path.exists(allowed_file):
        with open(allowed_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_allowed_groups(groups):
    with open(allowed_file, 'w', encoding='utf-8') as f:
        json.dump(groups, f, indent=4, ensure_ascii=False)


def add_allowed_group(chat_id):
    groups = load_allowed_groups()
    if chat_id not in groups:
        groups.append(chat_id)
        save_allowed_groups(groups)


def remove_allowed_group(chat_id):
    groups = load_allowed_groups()
    if chat_id in groups:
        groups.remove(chat_id)
        save_allowed_groups(groups)