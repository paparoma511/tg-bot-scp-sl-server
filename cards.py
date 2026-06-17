import random

CARDS = {
    "Common": [
        "Class-D",
        "Scientist",
        "Guard"
    ],

    "Rare": [
        "MTF Private",
        "Chaos Rifleman"
    ],

    "Epic": [
        "SCP-173",
        "SCP-049",
        "SCP-939"
    ],

    "Legendary": [
        "SCP-096",
        "SCP-106"
    ],

    "Mythic": [
        "SCP-682",
        "SCP-001"
    ]
}

WEIGHTS = {
    "Common": 60,
    "Rare": 25,
    "Epic": 10,
    "Legendary": 4,
    "Mythic": 1
}


def get_card():
    rarity = random.choices(
        list(WEIGHTS.keys()),
        weights=list(WEIGHTS.values())
    )[0]

    card = random.choice(CARDS[rarity])

    return rarity, card