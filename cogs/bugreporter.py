import discord
from discord.ext import commands, pages

class BugReportModal(discord.ui.Modal):
    def __init__(self, bot, owner_id):
        self.bot = bot
        self.owner_id = owner_id
        super().__init__(title="Bug Report Form")
        
        self.bug_title = discord.ui.InputText(
            label="Title",
            placeholder="Brief explanation of the bug",
            style=discord.InputTextStyle.short,
            required=True
        )
        self.add_item(self.bug_title)
        
        self.bug_description = discord.ui.InputText(
            label="Bug Description",
            placeholder="Please describe the bug in detail",
            style=discord.InputTextStyle.paragraph,
            required=True
        )
        self.add_item(self.bug_description)
        
    async def callback(self, interaction: discord.Interaction):
        bug_title = self.bug_title.value
        bug_description = self.bug_description.value
        author = interaction.user
        
        owner = self.bot.get_user(self.owner_id)

        if owner is not None:
            await owner.send(f"**Bug Reported by {author}**\n"
                             f"**Title**: {bug_title}\n"
                             f"**Description**: {bug_description}")
            
            await interaction.response.send_message("Thank you for your report! the bug has been submitted.", ephemeral=True)
        else:
            await interaction.response.send_message("Unable to send the bug report to the bot owner.", ephemeral=True)
            
class BugReport(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.slash_command(name="report_bug", description="Submit a bug report")
    async def report_bug(self, ctx: discord.ApplicationContext):
        owner_id = 232109327626797056
        modal = BugReportModal(bot=self.bot, owner_id=owner_id)
        
        await ctx.send_modal(modal)
        
def setup(bot):
    bot.add_cog(BugReport(bot))