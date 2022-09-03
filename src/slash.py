# Links
# https://docs.pycord.dev/en/master/api.html
# https://guide.pycord.dev/interactions/application-commands/slash-commands/

# Imports
import os
import discord
from dotenv import load_dotenv
import re

# Local Imports
from modules.dice import dice
from modules.dice import ob_dice

# Variables from .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DEBUG = os.getenv('DEBUG')
DEBUG_GUILDS = os.getenv('DEBUG_GUILDS')

# General Variables
description = """
Eon-Bot - https://github.com/obgr/eon-bot
"""

# Result vars for discord printout
string_rolled = "Rolled :"
string_total = "Total............ :"
string_rolls = "Rolls............ :"
string_sixes = "No. Sixes.... :"

if DEBUG_GUILDS is None:
    bot = discord.Bot()
elif DEBUG_GUILDS is not None:
    bot = discord.Bot(debug_guilds=[DEBUG_GUILDS])


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


# Commands
@bot.command(description="Sends the bot's latency.")
async def ping(ctx):
    await ctx.respond(f"Pong! Latency is {bot.latency}")


@bot.command(
    description="Scalable dice, Rolls a die in NdN+bonus or NtN format.")
async def roll(ctx, roll: discord.Option(str)):
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
        await ctx.respond("Format has to be in NtN+N, NtN, NdN+N or NdN")
        return

    # send results
    await ctx.respond(results)


@bot.command(
    description="""
    ob dice, Rolls two additional dice for each rolled six.
    Hardcoded for six sided dice.
    """)
async def ob(ctx, roll: discord.Option(str)):
    rollType = "ob"
    try:
        # Split roll to vars
        number_of_rolls, sides_to_die, bonus = splitRollString(
            roll,
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
            ROLL=roll.upper()
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
        await ctx.respond("Format has to be in Nd6+N, Nd6, Nt6+N or Nt6")
        return

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
    #     await ctx.message.add_reaction(emoji_die)
    #     await ctx.message.add_reaction(emoji_roll)
    # Send results
    await ctx.respond(results)


# Events
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(f"Latency is {bot.latency}")
    print(f"Debug is {DEBUG}")
    print(f"DEBUG_GUILDS is {DEBUG_GUILDS}")

bot.run(TOKEN)
