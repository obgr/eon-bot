#!/bin/python3

# Imports
import json
import random
import re
import sqlite3
from .dice import dice, ob_dice

# Result vars for discord printout
string_rolled = "Rolled :"
string_total = "Total ............:"
string_rolls = "Rolls ............:"
string_sixes = "No. Sixes ....:"


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


def sqlite_lookup(sqlite3_file: str, lookup: str, table: str, id: int):
    con = sqlite3.connect(sqlite3_file)
    cur = con.cursor()
    res = cur.execute(f"SELECT {lookup} FROM {table} WHERE ID IS '{id}'")
    result = res.fetchone()
    return result


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
        roll = roll.upper()

        # Build result string
        results = f"{string_rolled} {roll}\n"
        results = results + f"{string_rolls} {semiPrettyRolls}"
        if int(bonus) != 0:
            results = results + f"+ {bonus}\n"
        else:
            results = results + "\n"
        results = results + f"{string_total} {total}"
    except Exception as e:
        print(e)
        return 1
    return results


# Infinite Dice (ob dice)
def rollInfiniteDice(ob_roll: str, debug):
    rollType = "ob"
    try:
        # Removing blank spaces
        ob_roll = ob_roll.replace(" ", "") 
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
        ob_roll = ob_roll.upper()

        # Build result string
        results = f"{string_rolled} {ob_roll}\n"

        if sixes != 0:
            results = results + f"{string_sixes} {sixes}\n"
        results = results + f"{string_rolls} {pretty_rolls}"
        if int(bonus) != 0:
            results = results + f"+ {bonus}\n"
        else:
            results = results + "\n"
        results = results + f"{string_total} {total}"
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
        # Removing blank spaces
        ob_roll = ob_roll.replace(" ", "") 
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

        results = ""
        if ob_sixes != 0:
            results = results + f"OB No. Sixes :  {ob_sixes}\n"
        results = results + f"OB Rolls ........: {pretty_rolls}"
        if int(bonus) != 0:
            results = results + f"+ {bonus}\n"
        else:
            results = results + "\n"
        results = results + f"OB Total ........: {ob_total}\n"
        results = results + f"D100 ..............: {d100_total}\n"
    except Exception as e:
        print(e)
        return 1
    return results, d100_total


# Lookup tables
def lookupFunc(
    sqlite3_file: str,
    weapon_type: str,
    target: str,
    d100: int,
    debug: str
):
    # regexp for code
    # regex = r'[0-9]+(T|t|D|d)[0-9]+($|\+[0-9]+$)'
    # if re.match(regex, roll):
    #    if debug == "True":

    re_n = r'^(n+$|normal)+$'
    re_h = r'^(h+$|high)+$'
    re_l = r'^(l+$|low)+$'

    # regexp for weapon_type
    re_s = r'^(s+$|slash)+$'
    re_b = r'^(b+$|blunt)+$'
    re_r = r'^(r+$|range)+$'
    re_p = r'^(p+$|pierce)+$'

    # Lookup related vars
    lookup_table = "lookup_hit_table"
    lookup = "AREA, TARGET"

    # IF code
    if re.match(re_n, target, re.IGNORECASE):
        if debug == "True":
            print("matched normal")
        target = "CODE_NORMAL"
    elif re.match(re_h, target, re.IGNORECASE):
        if debug == "True":
            print("matched high")
        target = "CODE_HIGH"
    elif re.match(re_l, target, re.IGNORECASE):
        if debug == "True":
            print("matched low")
        target = "CODE_LOW"
    elif target is None:
        if debug == "True":
            print("code is None, defaulting to normal")
        target = "CODE_NORMAL"
    # define code to lookup
    else:
        print("target not matched")
        print(target)
        return 1

    # if weapon_type
    if re.match(re_s, weapon_type, re.IGNORECASE):
        if debug == "True":
            print("matched slash")
        hit_table = "hit_table_slash"
    elif re.match(re_b, weapon_type, re.IGNORECASE):
        if debug == "True":
            print("matched bluint")
        hit_table = "hit_table_blunt"
    elif re.match(re_r, weapon_type, re.IGNORECASE):
        if debug == "True":
            print("matched range")
        hit_table = "hit_table_range"
    elif re.match(re_p, weapon_type, re.IGNORECASE):
        if debug == "True":
            print("matched pierce")
        hit_table = "hit_table_pierce"
    elif weapon_type is None:
        if debug == "True":
            print("weapon_type is None, defaulting to slash")
        hit_table = "hit_table_slash"
    # define code to lookup
    else:
        print("weapon_type not matched")
        print(weapon_type)
        return 1

    hit_table_out = sqlite_lookup(
        sqlite3_file, target, hit_table, d100
    )
    hit_table_lookup = sqlite_lookup(
        sqlite3_file, lookup, lookup_table, hit_table_out[0]
    )
    return hit_table_lookup
