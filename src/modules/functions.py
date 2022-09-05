#!/bin/python3

# Imports
import re


# Functions
def prettifyDice(rolls):
    out = []
    for i in rolls:
        if i == "1":
            emoji = ":one:"
        elif i == "2":
            emoji = ":two:"
        elif i == "3":
            emoji = ":three:"
        elif i == "4":
            emoji = ":four:"
        elif i == "5":
            emoji = ":five:"
        elif i == "6":
            emoji = ":six:"
        else:
            emoji = i
        out.append(str(emoji))
    return ', '.join(out)


def splitRollString(roll: str, rollType: str, DEBUG):
    # Validate pattern
    if DEBUG == "True":
        print("\nRegex Debug")
    regex = r'[0-9]+(T|t|D|d)[0-9]+($|\+[0-9]+$)'
    if re.match(regex, roll):
        if DEBUG == "True":
            print("Regex matched")
    else:
        if DEBUG == "True":
            print("Regex NOT matched")
        return
    # Pattern to split: "[(T|t|D|d)+$]\s*"
    RollSplit = re.split(r"[(T|t|D|d)+$]\s*", roll)
    number_of_rolls = RollSplit[0]
    if rollType == "roll":
        sides_to_die = RollSplit[1]
    elif rollType == "ob":
        sides_to_die = 6
    if len(RollSplit) == 2:
        bonus = 0
    elif len(RollSplit) == 3:
        bonus = RollSplit[2]
    else:
        if DEBUG == "True":
            print("\nlen RollSplit Debug")
            print("len of RollSplit should only be 2 or 3")
            print("Len: ", len(RollSplit))
    # Validate content
    if DEBUG == "True":
        print("\nRollSplit Debug")
        print("Rolls : ", number_of_rolls)
        print("Sides : ", sides_to_die)
        print("Bonus : ", bonus)
    return number_of_rolls, sides_to_die, bonus
