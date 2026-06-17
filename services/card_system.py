import random
from data.cards import CARDS
from utils.randomizer import roll_rarity

def generate_cards(count=2):
    result = []

    for _ in range(count):
        rarity = roll_rarity()
        card = random.choice(CARDS[rarity])
        result.append((rarity, card))

    return result