# eon-bot

<img src="images/logo.png" >

- [eon-bot](#eon-bot)
  - [Licencing and acknowledgements](#licencing-and-acknowledgements)
  - [Hosting and Running the bot](#hosting-and-running-the-bot)
  - [Using the bot](#using-the-bot)
    - [Syntax](#syntax)
      - [/about - About](#about---about)
      - [/cs - Change status](#cs---change-status)
      - [/dm - Direct message](#dm---direct-message)
      - [/Ping - send Latency](#ping---send-latency)
      - [/roll - Scalable dice](#roll---scalable-dice)
      - [/ob or /inf - Infinite dice](#ob-or-inf---infinite-dice)
      - [/fight - Fight assistant](#fight---fight-assistant)
      - [/lookup - Lookup hit tables](#lookup---lookup-hit-tables)
      - [/if - Interactive Fight](#if---interactive-fight)
      - [/ir - Interactive Rolls](#ir---interactive-rolls)
      - [/qr - Queued Rolls](#qr---queued-rolls)
  - [Limitations](#limitations)

Discord dice roller bot for Eon, a tabletop RPG by Helmgast.
Rolls regular dice as well as whats known as an ob die (d6/t6) or infinite die (replace rolled six with two additional dice).

Written for python 3.10

## Licencing and acknowledgements

The project is published under the [MIT Licence](LICENSE.md).

The data bundled in [app/data/helmgast/](app/data/helmgast/) is created and owned by Helmgast AB.</br>
Permission has been granted by representatives of Helmgast AB to extract the hit table & damage table data from the books and bundle them in this project.

## Hosting and Running the bot

Read about [Hosting](docs/HOSTING.md) the bot

## Using the bot

Slash commands! You may use discord's slash commands in order to use the bot.

### Syntax

#### /about - About

eon-bot will send a link to the Github page.

#### /cs - Change status

eon-bot will change it's status to a random preset.

#### /dm - Direct message

eon-bot will send a direct message to the user.
Useful for secret dice rolls or lookups.

#### /Ping - send Latency

eon-bot will send a message containing the ping of the bot.

#### /roll - Scalable dice

Format has to be in NtN+N, NtN, NdN+N or NdN.

Can also be written with capital letters: ie NT6+N

Example

```bash
# Regular scalable dice
/roll 1d100
/roll 2T20+2
/roll 3d6+3

Output example:

```

#### /ob or /inf - Infinite dice

Format has to be in Nt6+N, Nt6, Nd6+N or Nd6.

if anything else than a 6 is supplied, it will be ignored. T6/D6 dice are hardcoded for the ob dice.

Can also be written with capital letters: ie NT6+N

Example

```bash
# ob dice
/ob 1t6
/ob 2T6+2
/ob 4d6+3

# This example will still use a six sided die.
/ob 4t8 +3

Output example:
Rolled : 4T6+3
No. Sixes.... : 2
Rolls............ : 2, 1, 3, 3, 4, 4+ 3
Total............ : 20
```

#### /fight - Fight assistant

Will roll ob +t100 dice for use in a fight.
User runs ```bash /fight <diceroll of weapon> <weapon_type> <aim>```

Example:

```bash
/fight 2t6+2 range

Output example:
OB Sixes ....: 1
OB Rolls ....: 5️⃣,2️⃣,5️⃣+ 2
OB Total ....: 14
D100 Total : 94

Aim: normal
Weapon type: range
Target: Höger ben, Vad
d100 Total...: 35
```

#### /lookup - Lookup hit tables

Work in progress - for now hit tables, damage tables to be added.
Supply your weapon type, aim (will rename this, normal, high, low) and the value of a rolled t100 and get where you hit.

Example:

```bash
/lookup <weapon_type> <aim> <t100>

weapon_type : slash/blunt/range/pierce
        or  : s/b/r/p
target      : normal/high/low
        or  : n/h/l
t100        : 1-100

Output example:
Command : /lookup weapon_type:r aim:l, t100:7
Target  : Torso, Bröstkorg

```

#### /if - Interactive Fight

Presents interactive dropdowns for fights.
Rolls a d100 and helps with finding the target based on choices.

#### /ir - Interactive Rolls

Presents buttons in a message which the users may press to make commmon dice rolls without bonuses.

#### /qr - Queued Rolls

Presents a modal where multiple dice rolls can be queued.

Type of dice: roll/normal/regular or ob/inf

List of rolls: supply a comma separated list of rolls, with or without bonus

Example:

```bash
Type of Dice: ob
List of rolls: 2t6+1,6t6+3,4t6,3t6+3
```

## Limitations

This bot is limited by the size of discord messages as well as sizes of some data types. Therefor, by design of the infinite dice, you may reroll a d6 500 times and hit these limits.

This is a known bug.

Accidentally summoning a cosmic horror monster on the outskirts of a semi-large town is not always appreciated by the dungeon master.
