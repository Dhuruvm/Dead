import discord
from discord.ext import commands

class unban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('unBan cog loaded')
        
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.User):
        """Command to unban a user"""
        guild = ctx.guild
        try:
            await guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
        except discord.Forbidden:
            await ctx.send("I do not have permission to unban this user.")
        except discord.HTTPException as e:
            await ctx.send(f"Failed to unban {user.mention}. Error: {e}")
        except Exception as e:
            await ctx.send(f"An unexpected error occurred: {e}")

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to use this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("User not found or invalid user provided.")
        else:
            await ctx.send(f"Command error: {error}")

async def setup(bot):
    await bot.add_cog(unban(bot))
