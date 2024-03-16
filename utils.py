from flask import g


def is_admin_check():
    if g.user_name and g.is_admin:
        return True
    else:
        return False


def is_user_check():
    if g.user_name and not g.is_admin:
        return True
    else:
        return False


def get_tags():
    return [
        "Comedy",
        "Action",
        "Thriller",
        "Horror",
        "Sci-Fi"
    ]


slots = {
    "slot_1": "9:00 AM",
    "slot_2": "12:00 PM",
    "slot_3": "4:00 PM",
    "slot_4": "7:00 PM"
}


def get_slots_list():
    return list(slots.keys())
