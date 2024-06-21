import discord
from discord.ext import commands
import asyncio

class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('ban cog loaded')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Command to ban a user"""
        try:
            embed = discord.Embed(
                title="You have been banned",
                description=f"You have been banned from **{ctx.guild.name}**.",
                color=discord.Color.red()
            )
            embed.add_field(name="Reason", value=reason if reason else "No reason provided.")
            await member.send(embed=embed)

            await member.ban(reason=reason)

            confirmation_embed = discord.Embed(
                title="User Banned",
                description=f"{member.mention} has been banned.",
                color=discord.Color.red()
            )
            confirmation_embed.add_field(name="Reason", value=reason if reason else "No reason provided.")
            await ctx.send(embed=confirmation_embed)
        except discord.Forbidden:
            await ctx.send("I do not have permission to ban this user.")
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

async def setup(bot):
    await bot.add_cog(Ban(bot))
