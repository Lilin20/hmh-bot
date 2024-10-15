import discord
from discord.ext import commands, pages
import sys
import os
import random

def getpath():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts')

sys.path.insert(1, getpath())
from database import database

class Profile(commands.Cog):
    """Module for the profile functions"""
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.startswith("https") or message.content.startswith("http"):
            return
        
        xp_to_give = len(message.content) - message.content.count(" ")
        database.add_xp(message.author.id, xp_to_give)
        leveling_info = database.get_leveling_info(message.author.id)
        
        calculated_xp = 50 * (1 + leveling_info[2]) ** int(leveling_info[0])
        if leveling_info[1] >= calculated_xp:
            database.level_up(message.author.id)
            
            embed = discord.Embed(
                title="✨ **Level Up!** ✨", 
                description=f"🎉 **{message.author.mention} has reached** **Level {leveling_info[0] + 1}!** 🏆",
                color=0x00ff00
            )
            embed.add_field(
                name="📈 **Progress to Next Level:**",     
                value="░░░░░░░░░░░░ [0%] - Resetted!",
                inline=False
            )
            embed.set_image(url="https://media1.tenor.com/m/FR8tb3ArfpMAAAAC/level-up-fantasy-bishoujo-juniku-ojisan-to.gif")
            embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4144/4144294.png")  # Cool level-up icon
            embed.set_footer(text="🚀 Keep grinding and become a legend!", icon_url="https://cdn-icons-png.flaticon.com/512/609/609803.png")
            await message.channel.send(embed=embed)
        
    @commands.slash_command()
    async def profile(self, ctx, member: discord.Member = None):
        """Shows your own profile or a profile from another user."""
        if member is None:
            member = ctx.author
            
        # 5% chance to be hijacked by Lain
        is_hijacked = random.random() < 0.025  # 5% chance
        
        # Normal kawaii profile
        if not is_hijacked:
            self.pages = [
                discord.Embed(
                    title=f"✨💖 Profile Inspector: {member.display_name} 💖✨",
                    description=f"**Status:** {database.get_status(member.id)}",
                    color=discord.Colour.nitro_pink()  # Cute pink color
                ).add_field(
                    name="👤 Name:", value=f"`{member.name}`", inline=True
                ).add_field(
                    name="🌸 Level:", value=f"`{str(database.get_level(member.id))}`", inline=True
                ).add_field(
                    name="🆔 ID:", value=f"`{str(member.id)}`", inline=True
                ).add_field(
                    name="💌 Messages:", value=f"`{str(database.get_message_count(member.id))}`", inline=True
                ).set_thumbnail(
                    url=member.avatar.url
                ).set_footer(
                    text=f"🎀 Joined: {member.joined_at.date()} • Created: {member.created_at.date()} 🎀"
                ),

                discord.Embed(
                    title="💎✨ Bank of HMH ✨💎",
                    description=f"Financial cuteness for {member.display_name} 💵",
                    color=discord.Color.teal()  # Different color for variation
                ).add_field(
                    name="⭐ Star-Coins:", value=f"`{str(database.get_balance(member.id))}` 💰", inline=True
                ).set_thumbnail(
                    url=member.avatar.url
                ).set_footer(
                    text="Keep stacking that kawaii cash! 🐰✨"
                ),
            ]

        # Lain Hijack version
        else:
            # Set Lain's avatar URL
            lain_avatar = "https://i1.sndcdn.com/artworks-e7qfjv4Ws4Pwdl98-Dc7FSQ-t500x500.jpg"  # Replace with another Lain image if you prefer
            
            self.pages = [
                discord.Embed(
                    title="📡 Profile... [Error Detected] 📡",
                    description="*\"Things aren't what they seem.\"*",
                    color=discord.Color.dark_red()  # Glitchy red color
                ).add_field(
                    name="👤 Name:", value="`lain.exe`", inline=True
                ).add_field(
                    name="🌐 Level:", value="`???`", inline=True
                ).add_field(
                    name="🆔 ID:", value="`404_NOT_FOUND`", inline=True
                ).add_field(
                    name="💌 Messages:", value="`Data Corrupted`", inline=True
                ).set_thumbnail(
                    url=lain_avatar  # Lain's avatar
                ).set_footer(
                    text=f"join date: --//-- • created: --//--",
                    icon_url=lain_avatar
                ).add_field(
                    name="👁️", value="*\"You are connected to the Wired...\"*", inline=False
                ),

                discord.Embed(
                    title="⚠️ Bank Records Unavailable ⚠️",
                    description="*\"Something went wrong...\"*",
                    color=discord.Color.dark_purple()  # Darker glitchy color
                ).add_field(
                    name="❌ Star-Coins:", value="`N/A`", inline=True
                ).set_thumbnail(
                    url=lain_avatar  # Lain's avatar
                ).set_footer(
                    text="Error: 0xL41N - Connection unstable 🧬"
                ),
            ]

        # Create a paginator and send the embeds
        paginator = pages.Paginator(pages=self.pages)
        await paginator.respond(ctx.interaction, ephemeral=False)
        
def setup(bot):
    bot.add_cog(Profile(bot))
        