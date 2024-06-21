import discord
from discord.ext import commands
import asyncio

class AntiNuke(commands.Cog):
        def __init__(self, bot):
            self.bot = bot
            self.recent_actions = {}  # Store recent actions by users

        @commands.Cog.listener()
        async def on_ready(self):
            print('AntiNuke cog loaded')

        @commands.Cog.listener()
        async def on_member_ban(self, guild, user):
            async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
                if entry.target == user:
                    await self.check_action(entry, action_type="ban")

        @commands.Cog.listener()
        async def on_member_remove(self, member):
            async for entry in member.guild.audit_logs(limit=1, action=discord.AuditLogAction.kick):
                if entry.target == member:
                    await self.check_action(entry, action_type="kick")

        @commands.Cog.listener()
        async def on_guild_channel_delete(self, channel):
            async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
                await self.check_action(entry, action_type="channel_delete")

        async def check_action(self, entry, action_type):
            user = entry.user

            # Initialize the user's action count if it doesn't exist
            if user.id not in self.recent_actions:
                self.recent_actions[user.id] = {"ban": 0, "kick": 0, "channel_delete": 0}

            # Increment the appropriate action count
            self.recent_actions[user.id][action_type] += 1

            # Define action limits
            limits = {"ban": 3, "kick": 3, "channel_delete": 3}

            # Check if the action exceeds the limit
            if self.recent_actions[user.id][action_type] >= limits[action_type]:
                await self.take_action(entry.guild, user, action_type)

            # Reset the action count after a certain period
            await asyncio.sleep(60)  # 1 minute reset time
            self.recent_actions[user.id][action_type] = 0  # Reset to 0 after timeout

        async def take_action(self, guild, user, action_type):
            try:
                await guild.ban(user, reason=f"Anti-Nuke: Exceeded {action_type} limit")
                log_channel = discord.utils.get(guild.text_channels, name="mod-log")
                if log_channel:
                    embed = discord.Embed(
                        title="User Banned",
                        description=f"{user.mention} was banned for exceeding {action_type} limit.",
                        color=discord.Color.red()
                    )
                    await log_channel.send(embed=embed)
            except discord.Forbidden:
                print(f"Failed to ban {user}. Insufficient permissions.")

async def setup(bot):
 await bot.add_cog(AntiNuke(bot))
