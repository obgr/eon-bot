#!/bin/python3
# dice.py
# Collection of dice
# dice = simple scalable dice
# ob_dice = Roll T6 dice, reroll two dice when rolling a 6.

import random

# Function for simple scalable die
def dice(number_of_rolls, bonus, sides_to_die):
    list_of_raw_rolls = []
    sum = 0
    total = 0

    if int(number_of_rolls) < 1:
        # Lowest number of rolls we handle is 1
        number_of_rolls = 1
        
    if int(sides_to_die) < 2:
        # Lowest die we handle is a T2
        sides_to_die = 2

    def roll(number_of_rolls, sides_to_die):
        for i in range(number_of_rolls):
            die=random.randint(1, int(sides_to_die))
            list_of_raw_rolls.append(str(die))
        return list_of_raw_rolls

    # Roll
    list_of_raw_rolls = roll(number_of_rolls, int(sides_to_die))

    # Sum dice rolls
    for i in list_of_raw_rolls:
        sum += int(i)

    # Total
    total = int(sum) + int(bonus)
    return sum, list_of_raw_rolls, total

# Function for ob dice
def ob_dice(number_of_rolls, bonus):
    list_of_ob_rolls = []
    list_of_sixes = []
    list_of_raw_rolls = []
    sum = 0
    sixes = 0
    total = 0

    if int(number_of_rolls) < 1:
        # Lowest number of rolls we handle is 1
        number_of_rolls = 1

    def roll(number_of_rolls):
        for i in range(number_of_rolls):
            die = random.randint(1, 6)
            if die == 6:
                list_of_sixes.append(str(die))
                list_of_raw_rolls.append(str(die))
                roll(2)
            else:
                list_of_ob_rolls.append(str(die))
                list_of_raw_rolls.append(str(die))
        return list_of_ob_rolls, list_of_raw_rolls, list_of_sixes

    # Roll
    list_of_ob_rolls, list_of_raw_rolls, list_of_sixes = roll(number_of_rolls)

    # Sum dice rolls
    for i in list_of_ob_rolls:
        sum += int(i)
    
    # count sixes
    sixes = len(list_of_sixes)

    # Total
    total = int(sum) + int(bonus)
    return sum, list_of_ob_rolls, list_of_raw_rolls, sixes, total