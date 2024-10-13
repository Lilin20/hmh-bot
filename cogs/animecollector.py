import discord
from discord.ext import commands
import sys
import os
import asyncio

def getpath():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts')

sys.path.insert(1, getpath())
from waifugen import get_random_anime_character
from database import database

class AnimeCharacterCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="collect", description="Gives you a random anime character to collect.")
    async def collect(self, ctx: discord.ApplicationContext):
        character = get_random_anime_character()

        if character:
            embed = discord.Embed(
                title=character["name"],
                description=character["description"],
                color=0x00ff00
            )
            embed.add_field(name="Anime Title (Romaji)", value=character["anime_title_romaji"], inline=False)
            embed.add_field(name="Anime Title (English)", value=character["anime_title_english"], inline=False)
            embed.set_image(url=character["image"])

            button_yes = discord.ui.Button(label="👍 Add to collection", style=discord.ButtonStyle.success, custom_id="extend_collection")
            button_no = discord.ui.Button(label="👎 Skip this one", style=discord.ButtonStyle.danger, custom_id="not_extend_collection")

            async def button_callback(interaction: discord.Interaction):
                if interaction.user != ctx.user:
                    await interaction.response.send_message("You are not allowed to steal characters from others.", ephemeral=True)
                    return
                
                button_yes.disabled = True
                button_no.disabled = True

                if interaction.data['custom_id'] == "extend_collection":
                    await interaction.response.send_message("You have added this character to your collection!", ephemeral=True)
                    database.add_anime_char(interaction.user.id, character["name"], character["anime_title_english"], character["anime_title_romaji"])
                    
                elif interaction.data['custom_id'] == "not_extend_collection":
                    await interaction.response.send_message("You skipped this character.", ephemeral=True)

                await interaction.message.edit(view=view)
                view.stop()

            button_yes.callback = button_callback
            button_no.callback = button_callback

            view = discord.ui.View()
            view.add_item(button_yes)
            view.add_item(button_no)

            await ctx.respond(embed=embed, view=view)

            await asyncio.sleep(10)
            if button_no.disabled != True:
                button_yes.disabled = True
                button_no.disabled = True
                
                await ctx.channel.send("The selection for this character has expired.")
                await ctx.edit(view=view)
                view.stop()

        else:
            await ctx.respond("There was an error while fetching a character. Please inform the developer.")

def setup(bot):
    bot.add_cog(AnimeCharacterCog(bot))
