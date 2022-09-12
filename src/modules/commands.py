#!/bin/python3

# Imports
from .dice import dice, ob_dice
from .functions import splitRollString, prettifyDice

# Result vars for discord printout
string_rolled = "Rolled :"
string_total = "Total............ :"
string_rolls = "Rolls............ :"
string_sixes = "No. Sixes.... :"


# Commands
# Regular scalable dice
def rollDice(roll: str, DEBUG):
    rollType = "roll"
    try:
        # Split roll to vars
        number_of_rolls, sides_to_die, bonus = splitRollString(
            roll,
            rollType,
            DEBUG
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
    except ValueError:
        return 1
    return results


# Infinite Dice (ob dice)
def rollInfiniteDice(ob_roll: str, DEBUG):
    rollType = "ob"
    print("here")
    try:
        print("here2")
        # Split roll to vars
        number_of_rolls, sides_to_die, bonus = splitRollString(
            ob_roll,
            rollType,
            DEBUG
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
    except ValueError:
        print("\nBad Roll Debug")
        print(sum_rolls)
        print(int(number_of_rolls))
        print(int(number_of_rolls) * 2)
        return 1

    # Debug some roll info for bad roll algorithm.
    if DEBUG == "True":
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
def rollForFight(ob_roll: str, DEBUG):
    rollType = "ob"
    try:
        # Split roll to vars
        number_of_rolls, sides_to_die, bonus = splitRollString(
            ob_roll,
            rollType,
            DEBUG
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
    except ValueError:
        return 1
    return results
