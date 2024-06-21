import discord
from discord.ext import commands

class Nick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Nick cog loaded')

    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, member: discord.Member, *, nickname=None):
        """Change or remove a member's nickname."""
        if not ctx.author.guild_permissions.manage_nicknames:
            error_embed = discord.Embed(
                color=discord.Color.red(),
                description="You must have `Manage Nicknames` permission to use this command."
            )
            await ctx.send(embed=error_embed)
            return

        if not ctx.guild.me.guild_permissions.manage_nicknames:
            error_embed = discord.Embed(
                color=discord.Color.red(),
                description="I must have `Manage Nicknames` permission to use this command."
            )
            await ctx.send(embed=error_embed)
            return

        try:
            if nickname:
                await member.edit(nick=nickname)
                success_embed = discord.Embed(
                    color=discord.Color.green(),
                    description=f"{member.mention}'s nickname has been successfully changed to {nickname}."
                )
            else:
                await member.edit(nick=None)
                success_embed = discord.Embed(
                    color=discord.Color.green(),
                    description=f"{member.mention}'s nickname has been successfully removed."
                )
            await ctx.send(embed=success_embed)
        except discord.Forbidden:
            error_embed = discord.Embed(
                color=discord.Color.red(),
                description=f"I may not have sufficient permissions or my highest role may not be above or the same as {member.mention}."
            )
            await ctx.send(embed=error_embed)
        except discord.HTTPException as err:
            error_embed = discord.Embed(
                color=discord.Color.red(),
                description=f"An error occurred: {err}"
            )
            await ctx.send(embed=error_embed)

async def setup(bot):
    await bot.add_cog(Nick(bot))
