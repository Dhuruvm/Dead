import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('welcome cog loaded')
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Customize your welcome message and embed here
        welcome_channel = discord.utils.get(member.guild.text_channels, name='welcome')
        if welcome_channel:
            embed = discord.Embed(
                title="Welcome to the Server!",
                description=f"Hello {member.mention}, welcome to **{member.guild.name}**!",
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=member.avatar.url)
            embed.add_field(name="Member Count", value=f"We now have {member.guild.member_count} members!", inline=False)
            embed.add_field(name="Rules", value="Please make sure to read the rules in the #rules channel.", inline=False)
            embed.set_image(url="https://example.com/welcome-banner.png")  # Replace with your own banner URL
            embed.set_footer(text="Enjoy your stay!", icon_url=member.guild.icon.url)

            await welcome_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Welcome(bot))