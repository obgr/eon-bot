#!/bin/python3

# Links
# https://docs.pycord.dev/en/master/api.html
# https://guide.pycord.dev/interactions/application-commands/slash-commands/

# Imports
# from cProfile import label
import os
import discord
from discord.ui import Select, View
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
    Fight assistant, rolls ob + t100 for target.
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


# https://guide.pycord.dev/interactions/ui-components/buttons
# buttons - Classify this

class ButtonView(discord.ui.View):
    @discord.ui.button(label="1d10", row=0, style=discord.ButtonStyle.grey, emoji="🎲")
    async def roll_1d10_button_callback(self, button, interaction):
        await interaction.response.send_message(f"{interaction.user} pressed {button.label}")

    @discord.ui.button(label="1d100", row=0, style=discord.ButtonStyle.grey, emoji="🎲")
    async def roll_1d100_button_callback(self, button, interaction):
        await interaction.response.send_message(f"{interaction.user} pressed {button.label}")

    @discord.ui.button(label="ob 1d6", row=1, style=discord.ButtonStyle.blurple, emoji="🎲")
    async def ob_1d6_button_callback(self, button, interaction):
        await interaction.response.send_message(f"{interaction.user} pressed {button.label}")

    @discord.ui.button(label="ob 2d6", row=1, style=discord.ButtonStyle.blurple, emoji="🎲")
    async def ob_2d6_button_callback(self, button, interaction):
        await interaction.response.send_message(f"{interaction.user} pressed {button.label}")

    @discord.ui.button(label="ob 3d6", row=1, style=discord.ButtonStyle.blurple, emoji="🎲")
    async def ob_3d6_button_callback(self, button, interaction):
        await interaction.response.send_message(f"{interaction.user} pressed {button.label}")

    @discord.ui.button(label="ob 4d6", row=1, style=discord.ButtonStyle.blurple, emoji="🎲")
    async def ob_4d6_button_callback(self, button, interaction):
        await interaction.response.send_message(f"{interaction.user} pressed {button.label}")

    @discord.ui.button(label="ob 5d6", row=2, style=discord.ButtonStyle.green, emoji="🎲")
    async def ob_5d6_button_callback(self, button, interaction):
        await interaction.response.send_message(f"{interaction.user} pressed {button.label}")

    @discord.ui.button(label="ob 6d6", row=2, style=discord.ButtonStyle.green, emoji="🎲")
    async def ob_6d6_button_callback(self, button, interaction):
        await interaction.response.send_message(f"{interaction.user} pressed {button.label}")

    @discord.ui.button(label="ob 7d6", row=2, style=discord.ButtonStyle.green, emoji="🎲")
    async def ob_7d6_button_callback(self, button, interaction):
        await interaction.response.send_message(f"{interaction.user} pressed {button.label}")

    @discord.ui.button(label="ob 8d6", row=2, style=discord.ButtonStyle.green, emoji="🎲")
    async def ob_8d6_button_callback(self, button, interaction):
        await interaction.response.send_message(f"{interaction.user} pressed {button.label}")


@bot.slash_command(description="Roll preset dice using buttons")
async def button(ctx):
    await ctx.respond("Press the dice you want to roll", view=ButtonView())

# Modal
# wants Message Content intent https://guide.pycord.dev/popular-topics/intents
# https://guide.pycord.dev/interactions/ui-components/modal-dialogs


# Dropdown Fight
# https://guide.pycord.dev/interactions/ui-components/dropdowns
# https://github.com/DenverCoder1/tutorial-discord-bot/blob/select-menu-help/modules/help/help_command.py
# https://github.com/Pycord-Development/pycord/tree/master/examples/views


# Defines a custom Select containing colour options
# that the user can choose. The callback function
# of this class is called when the user changes their choice.
class aimDropdown(discord.ui.Select):
    def __init__(self, bot_: discord.Bot):
        # For example, you can use self.bot to retrieve a user or perform other functions in the callback.
        # Alternatively you can use Interaction.client, so you don't need to pass the bot instance.
        self.bot = bot_
        # Set the options that will be presented inside the dropdown:
        options = [
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
        # The placeholder is what will be shown when no option is selected.
        # The min and max values indicate we can only pick one of the three options.
        # The options parameter, contents shown above, define the dropdown options.
        super().__init__(
            placeholder="Choose your favourite colour...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        await interaction.response.send_message(
            f"Your favourite colour is {self.values[0]}"
        )


class weaponTypeDropdown(discord.ui.Select):
    def __init__(self, bot_: discord.Bot):
        self.bot = bot_
        options = [  # Options
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
        super().__init__(
            placeholder="Choose your favourite colour...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Your favourite colour is {self.values[0]}"
        )


# Defines a simple View that allows the user to use the Select menu.
class ifightView(discord.ui.View):
    def __init__(self, bot_: discord.Bot):
        self.bot = bot_
        super().__init__()

        # Adds the dropdown to our View object
        # self.add_item(weaponTypeDropdown(self.bot))
        self.add_item(aimDropdown(self.bot))

        # Initializing the view and adding the dropdown can actually be done in a one-liner if preferred:
        # super().__init__(Dropdown(self.bot))
    async def on_timeout(self):
        # remove dropdown from message on timeout
        self.clear_items()
        #await self._help_command.response.edit(view=self)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return self._help_command.context.author == interaction.user


@bot.slash_command(descriprion="Interactive Fight")
async def ifight(ctx: discord.ApplicationContext):
    """Sends a message with our dropdown that contains colour options."""

    # Create the view containing our dropdown
    view = ifightView(bot)

    # Sending a message containing our View
    await ctx.respond("Pick your favourite colour:", view=view)


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
