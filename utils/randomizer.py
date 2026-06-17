import random
from data.cards import WEIGHTS

def roll_rarity():
    pool = []
    for rarity, weight in WEIGHTS.items():
        pool.extend([rarity] * weight)
    return random.choice(pool)