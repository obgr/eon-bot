#!/bin/python3

# Links
# https://docs.pycord.dev/en/master/api.html
# https://guide.pycord.dev/interactions/application-commands/slash-commands/

# Imports
import os
import discord
from dotenv import load_dotenv

# Local Imports
from modules.functions import rollDice, rollInfiniteDice, rollForFight

# Variables from .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DEBUG = os.getenv('DEBUG')
DEBUG_GUILDS = os.getenv('DEBUG_GUILDS')

if DEBUG_GUILDS is None:
    bot = discord.Bot()
elif DEBUG_GUILDS is not None:
    bot = discord.Bot(debug_guilds=[DEBUG_GUILDS])


# Commands
@bot.command(description="Sends the bot's latency.")
async def ping(ctx):
    await ctx.respond(f"Pong! Latency is {bot.latency}")


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
        if DEBUG == "True":
            print("Successfully sent DM!")
        await ctx.respond(reply)
    except ValueError:
        if DEBUG == "True":
            print("Unsuccessfull in sending DM")


@bot.command(
    description="""
    Scalable dice, Rolls a die in NdN+bonus or NtN format.
Example: /roll 1d100
"""
    )
async def roll(ctx, roll: discord.Option(str)):
    results = rollDice(roll, DEBUG)
    await ctx.respond(results)


@bot.command(
    description="""
    infinite dice. Replace sixes with two additional dice.
D6 only. Example: /ob 3d6+3
""")
async def inf(ctx, inf_roll: discord.Option(str)):
    results = rollInfiniteDice(inf_roll, DEBUG)
    await ctx.respond(results)


@bot.command(
    description="""
    ob dice. Replace sixes with two additional dice.
T6 only. Example: /ob 3d6+3
""")
async def ob(ctx, ob_roll: discord.Option(str)):
    results = rollInfiniteDice(ob_roll, DEBUG)
    await ctx.respond(results)


@bot.command(
    description="""
    Roll for Fight, rolls ob + t100 for hit.
Example: /fight 2t6+2
"""
    )
async def fight(ctx, ob_roll: discord.Option(str)):
    results = rollForFight(ob_roll, DEBUG)
    await ctx.respond(results)


# Events
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Eon"))
    print(f"Logged in as {bot.user}")
    print(f"Latency is {bot.latency}")
    print(f"Debug is {DEBUG}")
    if DEBUG == "True":
        print(f"DEBUG_GUILDS is {DEBUG_GUILDS}")

bot.run(TOKEN)
