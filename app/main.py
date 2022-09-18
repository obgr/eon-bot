#!/bin/python3

# Links
# https://docs.pycord.dev/en/master/api.html
# https://guide.pycord.dev/interactions/application-commands/slash-commands/

# Imports
import os
import discord
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
@bot.command(description="Sends the bot's latency.")
async def ping(ctx):
    await ctx.respond(f"Pong! Latency is {bot.latency}")


@bot.command(description="Change bot discord status to a random preset")
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


@bot.command(description="About Bot")
async def about(ctx):
    message = """
    Hi, My name is {BOT}.
You can find my source code below.
Eon-Bot - https://github.com/obgr/eon-bot
""".format(
        BOT=bot.user
    )
    await ctx.respond(message)


@bot.command(
    description="""
    Ask bot to send a DM. Useful for secret dice rolls.
"""
)
async def dm(ctx):
    message = """
    Hello,
You may send slash commands directly to me in this private chat.
"""
    reply = "You got a DM {AUTHOR}".format(
        AUTHOR=ctx.author
    )
    try:
        await ctx.author.send(message)
        if debug == "True":
            print("Successfully sent DM!")
        await ctx.respond(reply)
    except ValueError:
        if debug == "True":
            print("Unsuccessfull in sending DM")


@bot.command(
    description="""
    Scalable dice, Rolls a die in NdN+bonus or NtN format.
Example: /roll 1d100
"""
)
async def roll(ctx, roll: discord.Option(str)):
    results = rollDice(roll, debug)
    await ctx.respond(results)


@bot.command(
    description="""
    infinite dice. Replace sixes with two additional dice.
D6 only. Example: /ob 3d6+3
""")
async def inf(ctx, inf_roll: discord.Option(str)):
    results = rollInfiniteDice(inf_roll, debug)
    await ctx.respond(results)


@bot.command(
    description="""
    ob dice. Replace sixes with two additional dice.
T6 only. Example: /ob 3d6+3
""")
async def ob(ctx, ob_roll: discord.Option(str)):
    results = rollInfiniteDice(ob_roll, debug)
    await ctx.respond(results)


@bot.command(
    description="""
    Fight assistant, rolls ob + t100 for hit.
Example: /fight 5t6+2
"""
)
async def fight(ctx, ob_roll: discord.Option(str)):
    results = rollForFight(ob_roll, debug)
    await ctx.respond(results)


@bot.command(
    description="""
    Lookup values in the hit tables.
"""
)
async def lookup(
    ctx,
    weapon_type: discord.Option(str),
    aim: discord.Option(str),
    t100: discord.Option(int)
):
    out = lookupFunc(data_file, weapon_type, aim, t100, debug)
    results = f"""
Command : /lookup weapon_type:{weapon_type} aim:{aim}, t100:{t100}
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
