import random
import time

COOLDOWN = 60 * 60 * 24  # 24 часа

ADMINS = [123456789]  # твой ID

cards_by_rarity = {
    "🟢 Common": [
        "Class-D", "Scientist", "Facility Guard",
        "MTF Cadet", "Chaos Conscript", "Medkit"
    ],
    "🔵 Rare": [
        "MTF Private", "Chaos Rifleman", "SCP-049-2"
    ],
    "🟣 Epic": [
        "SCP-173", "SCP-049", "SCP-939", "E-11 Rifle"
    ],
    "🟡 Legendary": [
        "SCP-096", "SCP-106", "Micro H.I.D.", "O5 Keycard"
    ],
    "🔴 Mythic": [
        "SCP-001", "SCP-682", "SCP-999"
    ]
}

rarity_weights = [
    ("🟢 Common", 60),
    ("🔵 Rare", 25),
    ("🟣 Epic", 10),
    ("🟡 Legendary", 4),
    ("🔴 Mythic", 1),
]


def roll_rarity():
    pool = []
    for r, w in rarity_weights:
        pool.extend([r] * w)
    return random.choice(pool)


user_last_open = {}
user_cards = {}