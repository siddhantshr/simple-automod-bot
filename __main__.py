import json, discord, asyncio
from discord.ext import commands, tasks
import modules.lemmatizer as lemmatizer
import data.token as token

automod = commands.Bot(
    command_prefix="oa!"
)

automod.remove_command('help')

async def check_if_mod(author):
    if author.bot or author.guild_permissions.manage_messages or author.id == 711444754080071714:
        return True
    return False

async def filter_words(message: discord.Message):
    with open("data/filtered-words.json", 'r') as f:
        filtered_words = json.load(f)

    message = await lemmatizer.get_lemmatized_sentence(message.content)

    # Checking for words in the message sent
    for word in message:
        if word in filtered_words:
            return True

async def filter_invites(message):
    if message.channel.id in [818513424782852097, 818513423893397564, 818513422953349171]:
        return False
    message = await lemmatizer.get_lemmatized_sentence(message.content)
    if "discord.gg" in message or "invite.gg" in message or "discord.io" in message or "dsc.gg" in message or "discord.com/invite" in message:
        return True

async def filter_mentions(message):
    if len(message.raw_mentions) >= 5:
        return True

@automod.event
async def on_ready():
    print(f"Logged in as {automod.user}")
    statuses.start()

@tasks.loop(seconds=30)
async def statuses():
    status = [
        "Guarding over 🌊 Ocean's Paradise",
        "Protecting 🌊 Ocean's Paradise",
        "Watching Over 🌊 Ocean's Paradise"
    ]

    await automod.change_presence(activity=discord.Game(name=__import__("random").choice(status)),
                                status=discord.Status.dnd)

@automod.event
async def on_message(message):
    author = message.author

    if message.guild is None:
        return

    if await check_if_mod(author) == False:
        if await filter_words(message):
            try:
                await message.delete()
            except:
                pass
            await message.channel.send(f"{author.name}, that word is blacklisted", delete_after=5)

        if await filter_invites(message):
            try:
                await message.delete()
            except:
                pass
            await message.channel.send(f"{author.name}, no invite links allowed in this channel", delete_after=5)

        if await filter_mentions(message):
            try:
                await message.delete()
            except:
                pass

            await message.channel.send(f"{author.name}, you message cannot mention more \
than 5 users at once.", delete_after=5)

    await automod.process_commands(message)

automod.run(token.TOKEN)