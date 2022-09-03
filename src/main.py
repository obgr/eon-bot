# https://docs.pycord.dev/en/master/api.html
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import re

# Local Imports
from modules.dice import dice
from modules.dice import ob_dice

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('BOT_PREFIX')
DEBUG = os.getenv('DEBUG')
emoji_die = "\U0001F3B2"
emoji_roll = "\U0001F9FB"
emoji_bad_roll = "\U0001F9D9"

description = """
Eon-Bot - https://github.com/obgr/eon-bot
"""

# Result vars for discord printout
string_total = "Total.............:"
string_rolls = "Rolls............ :"
string_sixes = "No. Sixes.... :"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(PREFIX),
    description=description,
    intents=intents
    )
bot.connections = {}


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


def nick_or_username(ctx):
    # ctx.message.author
    # ctx.message.author.nick
    # ctx.message.author.id
    if hasattr(ctx.message.author, 'nick'):
        if ctx.message.author.nick is None:
            out = ctx.message.author
        elif ctx.message.author.nick is not None:
            out = ctx.message.author.nick
    else:
        out = ctx.message.author
    return out


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
        # If Null set to 0
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
async def ping(ctx: commands.Context):
    """Sends the bot's latency."""
    await ctx.send(f"Pong! Latency is {bot.latency}")


@bot.command()
async def syntax(ctx: commands.Context):
    """Shows example syntax"""
    syntax = """
    Hello There,
    Im your friendly neighborhood discord bot.

    This is my syntax
    ```
    # Regular scalable dice
    Format has to be in NtN+N, NtN, NdN+N or NdN.
    Can also be written with capital letters: ie NT6+N
    # Example
    {PREFIX}roll 1t100
    {PREFIX}roll 2T20+2
    {PREFIX}roll 3d6+3


    # ob dice
    Roll D6 die/dice, roll two additional dice per rolled 6.
    Format has to be in Nt6+N, Nt6, Nd6+N or Nd6.
    if anything else than a 6 is supplied, it will be ignored.
    T6/D6 dice are hardcoded for the ob dice.
    Can also be written with capital letters: ie NT6+N
    # Example
    {PREFIX}ob 1t6
    {PREFIX}ob 2T6+2
    {PREFIX}ob 4d6+3
    # This example will still use a six sided die.
    {PREFIX}ob 4t8
    ```
    """.format(PREFIX=PREFIX)
    await ctx.send(syntax)


@bot.command()
async def roll(ctx: commands.Context, roll: str):
    """
    Scalable dice, Rolls a die in NdN+bonus or NtN format.
    """
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
        user = nick_or_username(ctx)

        # Build result string
        results = "{USER} rolled {ROLL}\n".format(USER=user, ROLL=roll.upper())
        results = results + string_rolls + " {ROLLS}".format(
            ROLLS=semiPrettyRolls
            )
        if int(bonus) != 0:
            results = results + "+ {BONUS}\n".format(BONUS=bonus)
        else:
            results = results + "\n"
        results = results + string_total + " {TOTAL}".format(TOTAL=total)
    except ValueError:
        await ctx.send("Format has to be in NtN+N, NtN, NdN+N or NdN")
        return

    # react and send results
    await ctx.message.add_reaction(emoji_die)
    await ctx.message.add_reaction(emoji_roll)
    await ctx.send(results)


@bot.command()
async def ob(ctx: commands.Context, roll: str):
    """
    ob dice, Rolls two additional dice for each rolled six.
    """
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
        user = nick_or_username(ctx)

        # Build result string
        results = "{USER} rolled ob{ROLL}\n".format(
            USER=user, ROLL=roll.upper()
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
        await ctx.send("Format has to be in Nd6+N, Nd6, Nt6+N or Nt6")
        return

    # Debug some roll info for bad roll algorithm.
    if DEBUG == "True":
        print("\nBad Roll Debug")
        print(sum_rolls)
        print(int(number_of_rolls))
        print(int(number_of_rolls) * 2)
    # Determine if its a bad roll.
    if sum_rolls < (int(number_of_rolls) * 2):
        # React
        await ctx.message.add_reaction(emoji_bad_roll)
    else:
        # React
        await ctx.message.add_reaction(emoji_die)
        await ctx.message.add_reaction(emoji_roll)
    # Send results
    await ctx.send(results)


# Events
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(f"Latency is {bot.latency}")
    print(f"Debug is {DEBUG}")

# Run bot
bot.run(TOKEN)
