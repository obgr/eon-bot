#!/bin/python3

# Links
# https://docs.pycord.dev/en/master/api.html
# https://guide.pycord.dev/interactions/application-commands/slash-commands/

# Imports
import os
import discord
from discord.commands import option
from dotenv import load_dotenv

# Local Imports
from modules.functions import rollDice, rollInfiniteDice, rollForFight, getActivity, lookupFunc  # noqa: E501

# Variables from .env
load_dotenv()
token = os.getenv('discord_token')
debug = os.getenv('debug')
debug_guilds = os.getenv('debug_guilds')
# Data
activities_json_file = os.getenv('activities_json_file')
data_file = os.getenv('data_file')

if debug_guilds is None:
    bot = discord.Bot()
elif debug_guilds is not None:
    bot = discord.Bot(debug_guilds=[debug_guilds])


# Commands
@bot.slash_command(description="Sends the bot's latency.")
async def ping(ctx):
    await ctx.respond(f"Pong! Latency is {bot.latency}")


@bot.slash_command(description="Change bot discord status to a random preset")
async def cs(ctx):
    activity_type, activity = getActivity(activities_json_file)
    if activity_type == "playing":
        await bot.change_presence(
            status=discord.Status.online,
            activity=discord.Game(name=activity)
        )
    elif activity_type == "listening":
        await bot.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name=activity
            )
        )
    elif activity_type == "watching":
        await bot.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=activity
            )
        )
    else:
        print("Unsupported activity type")
    await ctx.respond(
        f"{activity_type} {activity}, give me some time to update my status."
    )


@bot.slash_command(description="About Bot")
async def about(ctx):
    message = f"""
    Hi, My name is {bot.user}.
You can find my source code below.
Eon-Bot - https://github.com/obgr/eon-bot
"""
    await ctx.respond(message)


@bot.slash_command(
    description="""
    Ask bot to send a Direct Message. Useful for secret dice rolls.
"""
)
async def dm(ctx):
    message = """
    Hello,
You may send slash commands directly to me in this private chat.
"""
    reply = f"You got a DM {ctx.author}"
    try:
        await ctx.author.send(message)
        if debug == "True":
            print("Successfully sent DM!")
        await ctx.respond(reply)
    except ValueError:
        if debug == "True":
            print("Unsuccessfull in sending DM")


@bot.slash_command(
    description="""
    Scalable dice, Rolls a die in NdN+bonus or NtN format.
Example: /roll 1d100
"""
)
@option(
    "roll",
    description="Example: 1d100 or 4d6",
    required=True
)
async def roll(
    ctx,
    roll: str
):
    results = rollDice(roll, debug)
    await ctx.respond(results)


@bot.slash_command(
    description="""
    infinite dice. Replace sixes with two additional dice.
D6 only. Example: /ob 3d6+3
""")
@option(
    "inf_roll",
    description="Example: 2d6+2",
    required=True
)
async def inf(
    ctx: discord.ApplicationContext,
    inf_roll: str
):
    results = rollInfiniteDice(inf_roll, debug)
    await ctx.respond(results)


@bot.slash_command(
    description="""
    ob dice. Replace sixes with two additional dice.
T6 only. Example: /ob 3d6+3
""")
@option(
    "ob_roll",
    description="Example: 2t6+2",
    required=True
)
async def ob(
    ctx,
    ob_roll: str
):
    results = rollInfiniteDice(ob_roll, debug)
    await ctx.respond(results)


@bot.slash_command(
    description="""
    Fight assistant, rolls ob + t100 for hit.
Example: /fight 5t6+2
"""
)
@option(
    "ob_roll",
    description="Example: 2t6+2",
    required=True
)
@option(
    "weapon_type",
    description="slash/blunt/pierce/range",
    required=True
)
@option(
    "aim",
    description="normal, high or low",
    required=False,
    default='normal'
)
async def fight(
    ctx,
    ob_roll: str,
    weapon_type: str,
    aim: str
):
    weapon_type = weapon_type.lower()
    aim = aim.lower()
    roll_out, d100 = rollForFight(ob_roll, debug)
    lookup_out = lookupFunc(data_file, weapon_type, aim, d100, debug)
    results = f"""
    {roll_out}
Aim: {aim}
Weapon type: {weapon_type}
Target: {lookup_out[0]}, {lookup_out[1]}
"""
    await ctx.respond(results)


@bot.slash_command(
    description="""
    Lookup values in the hit tables.
"""
)
@option(
    "weapon_type",
    description="slash/blunt/pierce/range",
    required=True
)
@option(
    "aim",
    description="normal, high or low",
    required=True
)
@option(
    "d100",
    description="Example: 42",
    required=True
)
async def lookup(
    ctx,
    weapon_type: str,
    aim: str,
    d100: int
):
    weapon_type = weapon_type.lower()
    aim = aim.lower()
    out = lookupFunc(data_file, weapon_type, aim, d100, debug)
    results = f"""
Command : /lookup weapon_type: {weapon_type} aim: {aim}, t100: {d100}
Target        : {out[0]}, {out[1]}
"""
    await ctx.respond(results)


# Events
@bot.event
async def on_ready():
    activity_type, activity = getActivity(activities_json_file)
    if activity_type == "playing":
        await bot.change_presence(
            status=discord.Status.online,
            activity=discord.Game(name=activity)
        )
    elif activity_type == "listening":
        await bot.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name=activity
            )
        )
    elif activity_type == "watching":
        await bot.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=activity
            )
        )
    else:
        print("Unsupported activity type")
    print(f"Logged in as {bot.user}")
    print(f"Latency is {bot.latency}")
    print(f"Activity is {activity_type}: {activity}")
    print(f"Debug is {debug}")
    if debug == "True":
        print(f"debug_guilds is {debug_guilds}")

bot.run(token)
