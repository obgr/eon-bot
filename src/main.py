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
emoji_die = "\U0001F3B2"
emoji_roll = "\U0001F9FB"
emoji_mage = "\U0001F9D9"
emoji_l = ":regional_indicator_l:"
emoji_o = ":regional_indicator_o:"
emoji_s = ":regional_indicator_s:"

description = """
Eon-Bot - https://github.com/obgr/eon-bot
"""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
 
bot = commands.Bot(command_prefix=commands.when_mentioned_or(PREFIX), description=description, intents=intents)
bot.connections = {}

# Functions
def prettifyDice(rolls):
    out =[]
    #out=""
    for i in rolls:
    #for x in range(len(i)): 
        if i == "1":
            emoji=":one:"
        elif i == "2":
            emoji=":two:"
        elif i == "3":
            emoji=":three:"
        elif i == "4":
            emoji=":four:"
        elif i == "5":
            emoji=":five:"
        elif i == "6":
            emoji=":six:"
        else:
            emoji=i
        out.append(str(emoji))
    return ', '.join(out)

def nick_or_username(ctx):
    #ctx.message.author
    #ctx.message.author.nick
    #ctx.message.author.id
    if hasattr(ctx.message.author, 'nick'):
        if ctx.message.author.nick == None:
            out = ctx.message.author
        elif ctx.message.author.nick != None:
            out = ctx.message.author.nick
    else:
        out = ctx.message.author
    return out

@bot.command()
async def syntax(ctx: commands.Context ):
    """Shows example syntax"""
    results = """
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
    if anything else than a 6 is supplied, it will be ignored. T6/D6 dice are hardcoded for the ob dice.
    Can also be written with capital letters: ie NT6+N
    # Example
    {PREFIX}ob 1t6
    {PREFIX}ob 2T6+2
    {PREFIX}ob 4d6+3
    # This example will still use a six sided die.
    {PREFIX}ob 4t8 
    ```
    """.format(PREFIX=PREFIX)
    await ctx.send(results)

@bot.command()
async def roll(ctx: commands.Context, roll: str):
    """
    Scalable dice, Rolls a die in NdN+bonus or NtN format.
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
        semiPrettyRolls=', '.join(raw_rolls)
        user = nick_or_username(ctx)

        results = "{USER} rolled {ROLL}\n".format(USER=user, ROLL=roll.upper() )
        results = results + "Rolls............ : {ROLLS}".format(ROLLS=semiPrettyRolls)
        if int(bonus) != 0:
            results = results + "+ {BONUS}\n".format(BONUS=bonus)
        else:
            results = results + "\n"
        results = results + "Total.............: {TOTAL}".format(TOTAL=total )
    except ValueError:
        await ctx.send("Format has to be in NtN+N, NtN, NdN+N or NdN")
        return

    await ctx.message.add_reaction(emoji_die)
    await ctx.message.add_reaction(emoji_roll)
    await ctx.send(results)

@bot.command()
async def ob(ctx: commands.Context, roll: str):
    """
    ob dice, Rolls two additional dice for each rolled six.
    """
    #print(ctx.message.author.id)
    #print(ctx.message.author)
    #print(ctx.message.author.nick)
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
        pretty_rolls=prettifyDice(ob_rolls)
        user = nick_or_username(ctx)     

        results = "{USER} rolled ob{ROLL}\n".format(USER=user, ROLL=roll.upper() )
        if sixes != 0:
            results = results + "No. Sixes.... : {SIXES}\n".format(SIXES=sixes)
        results = results + "Rolls............ : {ROLLS}".format(ROLLS=pretty_rolls)
        if int(bonus) != 0:
            results = results + "+ {BONUS}\n".format(BONUS=bonus)
        else:
            results = results + "\n"
        results = results + "Total.............: {TOTAL}".format(TOTAL=total )
    except ValueError:
        await ctx.send("Format has to be in Nd6+N, Nd6, Nt6+N or Nt6")
        return
    print(sum_rolls)
    print (int(RollSplit[0]))
    print(int(RollSplit[0]) * 2)
    if sum_rolls < (int(RollSplit[0]) * 2):
        await ctx.message.add_reaction(emoji_mage)
    else:
        await ctx.message.add_reaction(emoji_die)
        await ctx.message.add_reaction(emoji_roll)
    await ctx.send(results)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
 
bot.run(TOKEN)