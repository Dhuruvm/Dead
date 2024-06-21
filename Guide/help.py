import discord
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('cmd cog loaded')

    @commands.command()
    async def cmd(self, ctx):
        """Displays information about the bot and all commands"""
        embed = discord.Embed(
            title=f"{self.bot.user.name}'s Information",
            description=f"**Total Servers:** {len(self.bot.guilds)}\n"
                        f"**Developers:** devterminator69, leftdc..\n"
                        f"**Language:** Python",
            color=discord.Color.red()
        )

        embed.set_thumbnail(url=self.bot.user.avatar.url)

        view = InfoView(self.bot)
        await ctx.send(embed=embed, view=view)

class InfoView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Moderation", style=discord.ButtonStyle.primary)
    async def moderation_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title="Moderation Commands", color=discord.Color.blue())
        commands_list = self.get_commands_list('Moderation')
        embed.add_field(name="Commands", value=commands_list, inline=False)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Modals", style=discord.ButtonStyle.primary)
    async def modals_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title="Modals", color=discord.Color.green())
        # Assuming you have a way to list your modals
        modals_list = self.get_modals_list()
        embed.add_field(name="Modals", value=modals_list, inline=False)
        await interaction.response.edit_message(embed=embed, view=self)

    def get_commands_list(self, category):
        commands_list = ""
        for command in self.bot.commands:
            if command.cog_name == category:
                commands_list += f"**{command.name}** - {command.help}\n"
        return commands_list if commands_list else "No commands found."

    def get_modals_list(self):
        # Placeholder for actual modal listing logic
        return "Modal 1\nModal 2\nModal 3"

async def setup(bot):
    await bot.add_cog(Info(bot))
