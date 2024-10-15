import os
import discord
from discord.ext import commands
import scripts.database as db
from dotenv import load_dotenv

# Set intents
intents = discord.Intents.default()

# Create a bot instance
bot = commands.Bot(intents=intents.all())

# Global flag for mainentance mode (default: False)
maintenance_mode = True

# Function to check if the bot is in maintenance mode
def maintenance_check(ctx):
    global maintenance_mode
    # If maintenance mode is on, allow only the owner to use the commands
    if maintenance_mode and ctx.author.id != 232109327626797056:
        return False
    return True

@bot.check
def global_check(ctx):
    return maintenance_check(ctx)

# Load cogs
@bot.event
async def on_ready():
    """Event listener: executes when the on_ready event triggers."""
    
    print("""
*******************************************
            ♡〜٩( ˃́▿˂̀ )۶〜♡
        Lovingly created by Lilin
             ♡〜(ꈍᴗꈍ)〜♡
*******************************************
    """)
    
    print(f'Logged in. Starting boot procedure...')
    
    if maintenance_mode:
        await bot.change_presence(
            status=discord.Status.do_not_disturb, 
            activity=discord.Game(name="⚠️ Maintenance Mode"))
    else:
        await bot.change_presence(
            status=discord.Status.online, 
            activity=discord.Game(name="✅ All systems operational"))
    
    guild = None
    for guilds in bot.guilds:
        guild = guilds
    
    print("Checking for new users...")
    async for member in guild.fetch_members(limit=None):
        if member.id != 1295112164788535316:
            if not db.database.check_user(member.id):
                try:
                    db.database.add_user(member.id, member.name, 1, 0, 0.25, 0, 0)
                except:
                    pass

@bot.slash_command(name="toggle_maintenance", description="Toggle maintenance mode (Owner Only)")
@commands.check(lambda ctx: ctx.author.id == 232109327626797056)  # Only allow the owner to toggle
async def toggle_maintenance(ctx):
    global maintenance_mode
    maintenance_mode = not maintenance_mode  # Toggle the state
    status = "enabled" if maintenance_mode else "disabled"

    # Set the bot's presence based on the maintenance mode status
    if maintenance_mode:
        await bot.change_presence(
            status=discord.Status.do_not_disturb, 
            activity=discord.Game(name="⚠️ Maintenance Mode"))
    else:
        await bot.change_presence(
            status=discord.Status.online, 
            activity=discord.Game(name="✅ All systems operational"))

    await ctx.respond(f"Maintenance mode is now {status}.", ephemeral=True)

@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, discord.errors.CheckFailure):
        # Catch the CheckFailure and respond with a custom message
        if maintenance_mode:
            await ctx.respond("Sorry, the bot is currently in maintenance mode. Only the owner can use commands.", ephemeral=True)
        else:
            await ctx.respond("You do not have permission to use this command.", ephemeral=True)
    else:
        raise error  # Re-raise any other exceptions

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f'Module loaded: {filename[:-3]}')

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
# Start bot
bot.run(TOKEN)
