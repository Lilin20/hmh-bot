import os
import discord
from discord.ext import commands
import scripts.database as db

# Set intents
intents = discord.Intents.default()

# Create a bot instance
bot = commands.Bot(intents=intents.all())

# Load cogs
@bot.event
async def on_ready():
    """Event listener: executes when the on_ready event triggers."""
    print(f'Logged in as: {bot.user}')
    
    guild = None
    for guilds in bot.guilds:
        guild = guilds
    
    print("Checking for new users...")
    async for member in guild.fetch_members(limit=None):
        if member.id != 1295112164788535316:
            if not db.database.check_user(member.id):
                try:
                    db.database.add_user(member.id, member.name)
                except:
                    pass


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f'Module loaded: {filename[:-3]}')

# Start bot
bot.run('MTI5NTExMjE2NDc4ODUzNTMxNg.GDSkOx.m7jBhAwJM-b4SHVDLdrl_RqzcjmAOkjQOBfqpI')
