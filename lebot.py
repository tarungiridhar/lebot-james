import discord
from dotenv import load_dotenv
import os
import asyncio
import random

load_dotenv()
token = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

client = discord.Client(intents=intents)

random_messages = [
    "{mention} You ready to take on the challenge and sign with the Lakers? Let's make some history together! 👑🔥",
    "Yo {mention} you ready to take it to the next level with the LakeShow? 👑💯 We can do some special things together. Let's get it! #LakersFam",
    "Hey {mention} you know what time it is… Lakers need someone like you. You ready to make history with us? Let's run it! 💪🏾🔥👑",
    "{mention} you got the skills, we got the stage. Let's bring a championship to LA. You in? 🏀💯 #LakersLegacy",
    "Ayo, what you think about bringing that fire to the Lakers? Let's turn up the court together {mention}. 🔥👑 #NextLevel",
    "I see you out there {mention}… imagine that on the Lakers squad. You ready to dominate? 💪🏾🏆 #LakersForLife",
    "The opportunity is here {mention}… join the family and let's make some magic happen on that court. You in? 👑🔥",
    "{mention} I been watching your game, no doubt you'd be a perfect fit for the Lakers. Let's make history together. 🏀💯👑",
    "{mention}, let's make a move, my guy. Lakers Nation is waiting for you to join the dynasty. 🙌🏾💪🏾👑",
    "Yo {mention}! What's up, champ? The Lakers could use someone like you. Ready to make some noise in LA? 💥👑",
    "{mention} you got the skill, we got the spotlight. Let's build something special in LA. You down? 🏆🔥",
    "Yo {mention}, imagine running this thing together in LA. You ready to put the city on your back? 🙌🏾👑",
    "We got the pieces, now we need that one last piece. {mention}, you ready to join the Lakers and make history? 🔥🏀",
    "{mention} I see you've been grinding, now it's time to shine on the big stage with the Lakers. Let's get to work! 💯👑",
    "{mention} the spotlight is yours if you want it. The Lakers are waiting for someone like you. Ready to shine? ✨🏆",
    "Yo {mention}, it's time to level up. You ready to join the Lakers and show them how we do it? 👑🔥",
    "I see the vision {mention}. Let's take it to the next level with the Lakers. You with me? 🏀💯",
    "{mention} you got the talent, we got the legacy. Let's create something legendary in LA. You in? 🙌🏾👑",
    "The Lakers need that spark, {mention}. What you think about joining forces and taking it all the way? 💥🔥",
    "We're one piece away from something special. You ready to make history with the Lakers, {mention}? 🏆👑"
]

poll_messages = [
    "{mention} Lakers Nation, real talk—who's ready to join the squad and make history? Drop a 🔥 in the next minute if you're in! 🙌🏾👑🏆",
    "{mention} Alright, I need to know… who's down to take their game to the next level with the Lakers? Hit me with a 🔥 in the next minute if you're with it! 💥👑",
    "{mention} Poll time! Who's ready to bring that energy to the Lakers and help us win a chip? Hit 🔥 in the next minute if you're in! 🏆👑",
    "{mention} Lakers fam, let's see where y'all at—who's ready to be a part of this championship journey? Drop a 🔥 in the next minute if you're with us! 💯🔥",
    "{mention} I wanna know—who's ready to put on the purple and gold and chase greatness with the Lakers? Hit me with a 🔥 in the next minute if you're down! 👑💥",
    "{mention} Real quick, who's looking to join the Lakers and make some noise this season? Hit 🔥 in the next minute below if you're ready to roll! 💪🏾🔥",
    "{mention} Time for a poll: Who's ready to step up and be a part of something legendary with the Lakers? Drop a 🔥 in the next minute if you're ready to shine! 🏆💯",
    "{mention} Alright, Lakers Nation—who's all in? Ready to join the squad and run it back for another chip? Hit me with a 🔥 in the next minute if you're down! 🙌🏾👑",
    "{mention} Poll check: Who's ready to make an impact with the Lakers? Drop a 🔥 in the next minute if you're in and want to chase that ring! 🔥💯",
    "{mention} Lakers fam, quick poll—who's ready to bring that championship mentality to LA? If you're with it, hit me with a 🔥 in the next minute! 👑🔥",
    "{mention} Let's get a vote—who's down to take their game to the next level with the Lakers? Drop a 🔥 in the next minute if you're ready to make history! 🏆👑"
]

# Handles the buttons and response when mentioning a specific person
class YesNoView(discord.ui.View):
    def __init__(self, member: discord.Member):
        super().__init__(timeout=60)  # View will stop accepting interactions after 60 seconds
        self.member = member

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.success)
    async def yes_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.member:
            await interaction.response.send_message("We don't need you right now...", ephemeral=True)
            return
        await interaction.response.send_message(f"Yessir!! {self.member.mention} said YES! They said we couldn't do it… NOW LOOK!! 🙌🏾🔥👑 #WitnessGreatness", ephemeral=False)
        self.stop()

    @discord.ui.button(label="No", style=discord.ButtonStyle.danger)
    async def no_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.member:
            await interaction.response.send_message("We don't need you right now...", ephemeral=True)
            return
        await interaction.response.send_message(f"Man oh man… {self.member.mention} said no… they'll try to break you, but the marathon continues. 🙏🏾💯 #KeepGoing #OnToTheNextOne", ephemeral=False)
        self.stop()

# Handles the polls, buttons, and response
class PollView(discord.ui.View):
    def __init__(self, member: discord.Member):
        super().__init__(timeout=60)
        self.member = member
        self.yes_count = 0
        self.no_count = 0
        self.voters = set()
        self.message = None 

    @discord.ui.button(label="Yes 🔥", style=discord.ButtonStyle.success)
    async def yes_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id in self.voters:
            await interaction.response.send_message("You already voted!", ephemeral=True)
            return
        self.yes_count += 1
        self.voters.add(interaction.user.id)
        await interaction.response.send_message("Vote counted: Yes 🔥", ephemeral=True)

    @discord.ui.button(label="No ❌", style=discord.ButtonStyle.danger)
    async def no_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id in self.voters:
            await interaction.response.send_message("You already voted!", ephemeral=True)
            return
        self.no_count += 1
        self.voters.add(interaction.user.id)
        await interaction.response.send_message("Vote counted: No ❌", ephemeral=True)

    async def on_timeout(self):
        if self.yes_count > self.no_count:
            result_message = f"{self.yes_count} YES'... {self.no_count} NO's... y'all already know what it is!! It's a YES! Let's bring that fire to the Lakers and make history! 👑💥🏆"
        elif self.no_count > self.yes_count:
            result_message = f"{self.yes_count} yes'... {self.no_count} no's... man. That one hurts. Was really hoping for a different outcome. But hey… we keep pushing. 🙏🏾💔👑 #TrustTheJourney"

        else:
            result_message = f"{self.yes_count} YES'... {self.no_count} NO's... and... a tie?! Wow, the people can't make up their mind. Guess I'll have to decide this one myself. 👑💭🔥 #TheDecision"


        await self.message.channel.send(f"{result_message}")
        await self.message.edit(view=None)  # Disable buttons


# Initial message when joining a server
@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send("Appreciate the warm welcome!! Excited for what's ahead—let's get to it and make history together! 🙌🏾👑 #Blessed #LockedIn")
            break


# If a message is sent starting with "hey lebron" case insensitive, mentions the user responds with a lebron greeting
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.lower().startswith('hey lebron'):
        await message.channel.send(f"Yo {message.author.mention}, what's up! Always good to see the fam. Let's keep it movin'! 🙌🏾🔥")


# Begins loop
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    client.loop.create_task(send_random_content())

# Randomly sends a message or a poll between 1 min and 12 hours
@client.event
async def send_random_content():
    await client.wait_until_ready()
    while not client.is_closed():
        for guild in client.guilds:
            # Picks a random channel to send a message in
            channels = [ch for ch in guild.text_channels if ch.permissions_for(guild.me).send_messages]
            if not channels:
                continue
            channel = random.choice(channels)

            # Picks a random non bot member
            members = [m for m in guild.members if not m.bot]
            if not members:
                continue
            member = random.choice(members)

            if random.choice([True, False]):
                # Send regular message
                message_template = random.choice(random_messages)
                content = message_template.format(mention=member.mention)
                view = YesNoView(member)
                await channel.send(content=content, view=view)
            else:
                # Send poll
                # Create message and view
                message_template = random.choice(poll_messages)
                content = message_template.format(mention="@everyone")
                dummy_member = guild.me  # Not used in poll logic but needed for constructor

                view = PollView(dummy_member)
                poll_message = await channel.send(content=content, view=view)
                view.message = poll_message  # Set the message so we can edit/send later

        await asyncio.sleep(random.randint(60, 43200))  # Random wait between 1 min and 12 hours
        

client.run(token)