import discord
from discord.ext import commands

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Kick cog loaded')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kick a member from the server."""
        if member == ctx.message.author:
            await ctx.send("You cannot kick yourself!")
            return

        if reason is None:
            reason = "No reason provided."

        try:
            await member.kick(reason=reason)
            embed = discord.Embed(
                title="Member Kicked",
                description=f"{member.mention} has been kicked from the server.",
                color=discord.Color.red()
            )
            embed.add_field(name="Reason", value=reason)
            embed.set_footer(text=f"Action performed by {ctx.author}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("I do not have permission to kick this member.")
        except discord.HTTPException:
            await ctx.send("An error occurred while trying to kick this member.")

async def setup(bot):
    await bot.add_cog(Kick(bot))
