#!/bin/python3

# Links
# https://docs.pycord.dev/en/master/api.html
# https://guide.pycord.dev/interactions/application-commands/slash-commands/

# Imports
import os
import sys
import discord
from discord.commands import option
from dotenv import load_dotenv
from loguru import logger

# Local Imports
from modules.functions import rollDice, rollInfiniteDice, rollForFight, getActivity, lookupFunc  # noqa: E501
from modules.dice import dice

# Variables from .env
load_dotenv()
token = os.getenv('discord_token')
debug = os.getenv('debug', "False")
debug_guilds = os.getenv('debug_guilds')

# Data Files
activities_json_file = os.getenv('activities_json_file')
data_file = os.getenv('data_file')

# Load debug guilds if set
if debug_guilds is None:
    bot = discord.Bot()
elif debug_guilds is not None:
    bot = discord.Bot(debug_guilds=[debug_guilds])

# Logger settings
logger.remove()
if debug == "True":
    logger.add(sys.stderr, level="DEBUG")
elif debug == "False":
    logger.add(sys.stderr, level="INFO")
else:
    logger.add(sys.stderr, level="INFO")
    logger.info("Debug not \"True\" or \"False\", defaulting to loglevel INFO")


# Commands
@logger.catch
@bot.slash_command(description="Sends the bot's latency.")
async def ping(ctx):
    latency = bot.latency
    logger.info(f"Pong! Latency is {latency}")
    await ctx.respond(f"Pong! Latency is {latency}")


@logger.catch
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
        logger.debug("Unsupported activity type")
    logger.info(f"Changing activity to {activity_type}: {activity}")
    await ctx.respond(
        f"{activity_type} {activity}, give me some time to update my status."
    )


@logger.catch
@bot.slash_command(description="About Bot")
async def about(ctx):
    message = f"Hi, My name is {bot.user}.\nYou can find my source code below.\nEon-Bot - https://github.com/obgr/eon-bot"
    await ctx.respond(message)


@logger.catch
@bot.slash_command(
    description="Ask bot to send a Direct Message. Useful for secret dice rolls."
)
async def dm(ctx):
    message = "Hello,\nYou may send slash commands directly to me in this private chat."
    reply = f"You got a DM {ctx.author}"
    try:
        await ctx.author.send(message)
        logger.debug("DM sent")
        await ctx.respond(reply)
    except Exception as e:
        logger.info("")
        logger.debug(f"Exception: {e}")


@logger.catch
@bot.slash_command(
    description="Scalable dice, Rolls a die in NdN+bonus or NtN format.\nExample: /roll 1d100"
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


@logger.catch
@bot.slash_command(
    description="infinite dice. Replace sixes with two additional dice.\nD6 only. Example: /ob 3d6+3")
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


@logger.catch
@bot.slash_command(
    description="ob dice. Replace sixes with two additional dice.\nT6 only. Example: /ob 3d6+3")
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


@logger.catch
@bot.slash_command(
    description="Fight assistant, rolls ob + t100 for target.\nExample: /fight 5t6+2"
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
    results = f"{roll_out}\nWeapon type: {weapon_type}\nAim: {aim}\nTarget: {lookup_out[0]}, {lookup_out[1]}"
    await ctx.respond(results)


@logger.catch
@bot.slash_command(
    description="Lookup values in the hit tables."
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
    results = f"Command : /lookup weapon_type: {weapon_type} aim: {aim}, t100: {d100}\nTarget        : {out[0]}, {out[1]}"
    await ctx.respond(results)


# https://guide.pycord.dev/interactions/ui-components/buttons
class interactiveRollView(discord.ui.View):
    @logger.catch
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(content="View timed out! Disabled all the components.", view=self)

    @discord.ui.button(label="1d10", row=0, style=discord.ButtonStyle.grey, emoji="🎲")
    async def roll_1d10_button_callback(self, button, interaction):
        roll = "1d10"
        results = rollDice(roll, debug)
        await interaction.response.send_message(
            f"{interaction.user} {results}"
        )

    @discord.ui.button(label="1d100", row=0, style=discord.ButtonStyle.grey, emoji="🎲")
    async def roll_1d100_button_callback(self, button, interaction):
        roll = "1d100"
        results = rollDice(roll, debug)
        await interaction.response.send_message(
            f"{interaction.user} {results}"
        )

    @discord.ui.button(label="ob 1d6", row=1, style=discord.ButtonStyle.blurple, emoji="🎲")
    async def ob_1d6_button_callback(self, button, interaction):
        ob_roll = "1d6"
        results = rollInfiniteDice(ob_roll, debug)
        await interaction.response.send_message(
            f"{interaction.user} {results}"
        )

    @discord.ui.button(label="ob 2d6", row=1, style=discord.ButtonStyle.blurple, emoji="🎲")
    async def ob_2d6_button_callback(self, button, interaction):
        ob_roll = "2d6"
        results = rollInfiniteDice(ob_roll, debug)
        await interaction.response.send_message(
            f"{interaction.user} {results}"
        )

    @discord.ui.button(label="ob 3d6", row=1, style=discord.ButtonStyle.blurple, emoji="🎲")
    async def ob_3d6_button_callback(self, button, interaction):
        ob_roll = "3d6"
        results = rollInfiniteDice(ob_roll, debug)
        await interaction.response.send_message(
            f"{interaction.user} {results}"
        )

    @discord.ui.button(label="ob 4d6", row=1, style=discord.ButtonStyle.blurple, emoji="🎲")
    async def ob_4d6_button_callback(self, button, interaction):
        ob_roll = "4d6"
        results = rollInfiniteDice(ob_roll, debug)
        await interaction.response.send_message(
            f"{interaction.user} {results}"
        )

    @discord.ui.button(label="ob 5d6", row=2, style=discord.ButtonStyle.green, emoji="🎲")
    async def ob_5d6_button_callback(self, button, interaction):
        ob_roll = "5d6"
        results = rollInfiniteDice(ob_roll, debug)
        await interaction.response.send_message(
            f"{interaction.user} {results}"
        )

    @discord.ui.button(label="ob 6d6", row=2, style=discord.ButtonStyle.green, emoji="🎲")
    async def ob_6d6_button_callback(self, button, interaction):
        ob_roll = "6d6"
        results = rollInfiniteDice(ob_roll, debug)
        await interaction.response.send_message(
            f"{interaction.user} {results}"
        )

    @discord.ui.button(label="ob 7d6", row=2, style=discord.ButtonStyle.green, emoji="🎲")
    async def ob_7d6_button_callback(self, button, interaction):
        ob_roll = "7d6"
        results = rollInfiniteDice(ob_roll, debug)
        await interaction.response.send_message(
            f"{interaction.user} {results}"
        )

    @discord.ui.button(label="ob 8d6", row=2, style=discord.ButtonStyle.green, emoji="🎲")
    async def ob_8d6_button_callback(self, button, interaction):
        ob_roll = "8d6"
        results = rollInfiniteDice(ob_roll, debug)
        await interaction.response.send_message(
            f"{interaction.user} {results}"
        )


@logger.catch
@bot.slash_command(description="Interactive Rolls - Roll preset dice using buttons")
async def ir(ctx):
    await ctx.respond("Press the dice you want to roll.", view=interactiveRollView(timeout=300))


# Intyeractive Fight
# https://guide.pycord.dev/interactions/ui-components/dropdowns
# https://github.com/DenverCoder1/tutorial-discord-bot/blob/select-menu-help/modules/help/help_command.py
# https://github.com/Pycord-Development/pycord/tree/master/examples/views
class interactiveFightView(discord.ui.View):
    @logger.catch
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(content="View timed out! Disabled all the components.", view=self)

    @logger.catch
    @discord.ui.select(
        row=0,
        placeholder="Where do you aim?",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(
                label="Normal", description="Think Different.", emoji="🔷"
            ),
            discord.SelectOption(
                label="High", description="Hello there!", emoji="🟥"
            ),
            discord.SelectOption(
                label="Low", description="#Ydoran, Left foot is a great target!", emoji="🟢"
            ),
        ]
    )
    async def selectAim_callback(self, select, interaction):
        # select.disabled = True  # set the status of the select as disabled
        self.selectAim = select.values[0]
        await interaction.response.edit_message(view=self)

    @logger.catch
    @discord.ui.select(
        row=1,
        placeholder="Choose weapon type",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(
                label="Slash", description="Regular slice!", emoji="⚔️"
            ),
            discord.SelectOption(
                label="Blunt", description="Me Strong, Me angry!", emoji="🔨"
            ),
            discord.SelectOption(
                label="Pierce", description="Stick them with the pointy end!", emoji="🪡"
            ),
            discord.SelectOption(
                label="Range", description="Spooky knife action at a distance?", emoji="🏹"
            )
        ]
    )
    async def selectWeaponType_callback(self, select, interaction):
        # select.disabled = True  # set the status of the select as disabled
        self.selectWeaponType = select.values[0]
        await interaction.response.edit_message(view=self)

    @logger.catch
    @discord.ui.button(
        row=2,
        label="Submit",
        style=discord.ButtonStyle.blurple,
        emoji="☑"
    )
    async def button_callback(self, button, interaction):
        # roll_out, d100 = rollForFight(ob_roll, debug)
        _, _, d100 = dice(
            int(1),
            int(0),
            int(100)
        )
        lookup_out = lookupFunc(data_file, self.selectWeaponType.lower(), self.selectAim.lower(), d100, debug)
        results = f"Weapon type: {self.selectWeaponType.lower()}\nAim: {self.selectAim.lower()}\nRoll: {d100}\nTarget: {lookup_out[0]}, {lookup_out[1]}"
        await interaction.response.send_message(results)


@logger.catch
@bot.slash_command()
async def ifight(ctx):
    """Pressents interactive dropdowns for fights, helps finding a target"""
    await ctx.respond("Make your selection", view=interactiveFightView(timeout=180))


# Queued rolls
class QueuedRollsModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Type of Dice"))
        self.add_item(discord.ui.InputText(label="List of Rolls", style=discord.InputTextStyle.long))

    @logger.catch
    async def callback(self, interaction: discord.Interaction):
        rollType = self.children[0].value
        listRolls = self.children[1].value.split(",")
        logger.info(f"{rollType}")
        logger.info(f"{listRolls}")

        results = ""
        if rollType.lower() == "ob" or rollType.lower() == "inf":
            # Roll infinite/ob dice
            for i in listRolls:
                results = results + rollInfiniteDice(i, debug) + "\n\n"
        elif rollType.lower() == "normal" or rollType.lower() == "regular" or rollType.lower() == "roll":
            # roll a regular dice
            for i in listRolls:
                results = results + rollDice(i, debug)
        else:
            results = f"Unknown rollType: {rollType}"

        await interaction.response.send_message(results)


@logger.catch
@bot.slash_command()
async def qr(ctx: discord.ApplicationContext):
    """Opens a modal for Queued Rolls (comma separated)"""
    modal = QueuedRollsModal(title="Queued Rolls")
    await ctx.send_modal(modal)


# Events
@logger.catch
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
        logger.info("Unsupported activity type")
    logger.info(f"Logged in as {bot.user}")
    logger.info(f"Latency is {bot.latency}")
    logger.info(f"Current activity is {activity_type}: {activity}")
    logger.info(f"Debug: {debug}")
    logger.debug(f"debug_guilds: {debug_guilds}")

bot.run(token)
