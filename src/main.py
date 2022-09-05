#!/bin/python3
# Links
# https://docs.pycord.dev/en/master/api.html
# https://guide.pycord.dev/interactions/application-commands/slash-commands/

# Imports
import os
import discord
from dotenv import load_dotenv

# Local Imports
from modules.dice import dice
from modules.dice import ob_dice
from modules.functions import prettifyDice
from modules.functions import splitRollString

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


# Commands
@bot.command(description="Sends the bot's latency.")
async def ping(ctx):
    await ctx.respond(f"Pong! Latency is {bot.latency}")


@bot.command(
    description="""
    Scalable dice, Rolls a die in NdN+bonus or NtN format.
    Example: /roll 1d100
    """
    )
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
    ob dice, replace sixes with two additional dice.
    D6 Hardcoded. Example: /ob 3t6+3
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


@bot.command(
    description="""
    Roll for Fight, rolls ob + t100 for hit.
    Example: /fight 2t6+2
    """
    )
async def fight(ctx, roll: discord.Option(str)):
    rollType = "ob"
    try:
        # Split roll to vars
        number_of_rolls, sides_to_die, bonus = splitRollString(
            roll,
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
        await ctx.respond("Format has to be in NtN+N, NtN, NdN+N or NdN")
        return

    # send results
    await ctx.respond(results)


# Events
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(f"Latency is {bot.latency}")
    print(f"Debug is {DEBUG}")
    print(f"DEBUG_GUILDS is {DEBUG_GUILDS}")

bot.run(TOKEN)
