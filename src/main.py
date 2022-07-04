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

description = """
Eon-Bot - 
"""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
 
bot = commands.Bot(command_prefix=commands.when_mentioned_or(PREFIX), description=description, intents=intents)
bot.connections = {}
 
@bot.command()
async def roll(ctx: commands.Context, roll: str):
    """
    Scalable dice roller
    Rolls a die in NtN+bonus or NtN format.
    Example: 4t6+2 or 1t100 
    """
    try:
         # Pattern to split: "[(T|t|D|d)+$]\s*"
        RollSplit = re.split(r"[(T|t|D|d)+$]\s*", roll)
        number_of_rolls=RollSplit[0]
        sides_to_die=RollSplit[1]
        if len(RollSplit) == 2:
            # If Null set to 0
            bonus=0
        elif len(RollSplit) == 3:
            bonus=RollSplit[2]
        else:
            print("len of RollSplit should only be 2 or 3")
            print("Len: ", len(RollSplit))
        sum_rolls, raw_rolls, total = dice(int(number_of_rolls), int(bonus), int(sides_to_die))
        results = { "sum_rolls": sum_rolls, "raw_rolls": raw_rolls, "total": total }

    except ValueError:
        await ctx.send("Format has to be in NtN+N, NtN, NdN+N or NdN")
        return
    
    await ctx.send(results)

@bot.command()
async def ob(ctx: commands.Context, roll: str):
    """Rolls a die in Nt6+bonus format."""
    try:
        # Pattern to split: "[(T|t|D|d)+$]\s*"
        RollSplit = re.split(r"[(T|t|D|d)+$]\s*", roll)
        number_of_rolls=RollSplit[0]
        #sides_to_die=RollSplit[1]
        if len(RollSplit) == 2:
            # If Null set to 0
            bonus=0
        elif len(RollSplit) == 3:
            bonus=RollSplit[2]
        else:
            print("len of RollSplit should only be 2 or 3")
            print("Len: ", len(RollSplit))
        sum_rolls, ob_rolls, raw_rolls, sixes, total = ob_dice(int(number_of_rolls), int(bonus))
        results = { "sum_rolls": sum_rolls, "ob_rolls": ob_rolls, "raw_rolls": raw_rolls,"sixes": sixes, "total": total }

    except ValueError:
        await ctx.send("Format has to be in Nt6+N, Nt6, Nd6+N or Nd6")
        return

    #sum_rolls, ob_rolls, raw_rolls, sixes, total = ob_dice(int(number_of_rolls), int(bonus))
    #results = { "sum_rolls": sum_rolls, "ob_rolls": ob_rolls, "raw_rolls": raw_rolls,"sixes": sixes, "total": total }
    await ctx.send(results)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
 
bot.run(TOKEN)