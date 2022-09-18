#!/bin/python3

# Imports
import json
import random
import re
from .dice import dice, ob_dice

# Result vars for discord printout
string_rolled = "Rolled :"
string_total = "Total............ :"
string_rolls = "Rolls............ :"
string_sixes = "No. Sixes.... :"


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


def splitRollString(roll: str, rollType: str, debug):
    # Validate pattern
    if debug == "True":
        print("\nRegex Debug")
    regex = r'[0-9]+(T|t|D|d)[0-9]+($|\+[0-9]+$)'
    if re.match(regex, roll):
        if debug == "True":
            print("Regex matched")
    else:
        if debug == "True":
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
        if debug == "True":
            print("\nlen RollSplit Debug")
            print("len of RollSplit should only be 2 or 3")
            print("Len: ", len(RollSplit))
    # Validate content
    if debug == "True":
        print("\nRollSplit Debug")
        print(f"Rolls : {number_of_rolls}")
        print(f"Sides : {sides_to_die}")
        print(f"Bonus : {bonus}")
    return number_of_rolls, sides_to_die, bonus


def getActivity(filepath: str):
    with open(filepath) as json_file:
        data = json.load(json_file)
        # Get random element
        random_element = random.choice(list(data.keys()))
        # Get random child from randomized element
        random_child = random.choice(list(data[random_element]['activities']))
    return random_element, random_child


# Command functions
# Regular scalable dice
def rollDice(roll: str, debug):
    rollType = "roll"
    try:
        # Split roll to vars
        number_of_rolls, sides_to_die, bonus = splitRollString(
            roll,
            rollType,
            debug
            )
        # Roll the dice
        sum_rolls, raw_rolls, total = dice(
            int(number_of_rolls),
            int(bonus),
            int(sides_to_die)
            )

        # Make Pretty
        semiPrettyRolls = ', '.join(raw_rolls)

        # Build result string
        results = string_rolled + " {ROLL}\n".format(
            ROLL=roll.upper()
            )
        results = results + string_rolls + " {ROLLS}".format(
            ROLLS=semiPrettyRolls
            )
        if int(bonus) != 0:
            results = results + "+ {BONUS}\n".format(BONUS=bonus)
        else:
            results = results + "\n"
        results = results + string_total + " {TOTAL}".format(TOTAL=total)
    except Exception as e:
        print(e)
        return 1
    return results


# Infinite Dice (ob dice)
def rollInfiniteDice(ob_roll: str, debug):
    rollType = "ob"
    try:
        # Split roll to vars
        number_of_rolls, sides_to_die, bonus = splitRollString(
            ob_roll,
            rollType,
            debug
            )
        # Roll the dice
        sum_rolls, ob_rolls, raw_rolls, sixes, total = ob_dice(
            int(number_of_rolls),
            int(bonus)
            )
        # Make Pretty
        pretty_rolls = prettifyDice(ob_rolls)

        # Build result string
        results = string_rolled + " {ROLL}\n".format(
            ROLL=ob_roll.upper()
            )

        if sixes != 0:
            results = results + string_sixes + " {SIXES}\n".format(
                SIXES=sixes
                )
        results = results + string_rolls + " {ROLLS}".format(
            ROLLS=pretty_rolls
            )
        if int(bonus) != 0:
            results = results + "+ {BONUS}\n".format(
                BONUS=bonus
                )
        else:
            results = results + "\n"

        results = results + string_total + " {TOTAL}".format(
            TOTAL=total
            )
    except Exception as e:
        print(e)
        print("\nBad Roll Debug")
        print(sum_rolls)
        print(int(number_of_rolls))
        print(int(number_of_rolls) * 2)
        return 1

    # Debug some roll info for bad roll algorithm.
    if debug == "True":
        print("\nBad Roll Debug")
        print(sum_rolls)
        print(int(number_of_rolls))
        print(int(number_of_rolls) * 2)

    # Determine if its a bad roll.
    # if sum_rolls < (int(number_of_rolls) * 2):
    #     # React
    #     await ctx.message.add_reaction(emoji_bad_roll)
    # else:
    #     # React
    return results


# Fight, rolls a bunch of things you need for a fight in eon.
def rollForFight(ob_roll: str, debug):
    rollType = "ob"
    try:
        # Split roll to vars
        number_of_rolls, sides_to_die, bonus = splitRollString(
            ob_roll,
            rollType,
            debug
            )

        # Roll the ob/infinite dice
        ob_sum_rolls, ob_rolls, ob_raw_rolls, ob_sixes, ob_total = ob_dice(
            int(number_of_rolls),
            int(bonus)
            )

        # Roll the t100 die

        d100_sum_rolls, d100_raw_rolls, d100_total = dice(
            int(1),
            int(0),
            int(100)
            )

        # Make Pretty
        pretty_rolls = prettifyDice(ob_rolls)
        # semiPrettyRolls = ', '.join(d100_raw_rolls)

        # Build result string
        # results = string_rolled + " {ROLL}\n".format(
        #    ROLL=roll.upper()
        #    )
        results = "OB Rolls.....: {ROLLS}".format(
            ROLLS=pretty_rolls
            )
        if int(bonus) != 0:
            results = results + "+ {BONUS}\n".format(BONUS=bonus)
        else:
            results = results + "\n"
        results = results + "OB Total.....: {TOTAL}\n".format(TOTAL=ob_total)
        results = results + "d100 Total : {TOTAL}\n".format(TOTAL=d100_total)
    except Exception as e:
        print(e)
        return 1
    return results
