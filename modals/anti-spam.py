import discord
from discord.ext import commands
import asyncio
from collections import defaultdict, deque
import time

class AntiSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_messages = defaultdict(lambda: deque(maxlen=5))
        self.spam_threshold = 5  # Number of messages considered spam within the interval
        self.time_interval = 10  # Time interval in seconds

    @commands.Cog.listener()
    async def on_ready(self):
        print('AntiSpam cog loaded')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        current_time = time.time()
        self.user_messages[message.author.id].append(current_time)

        if len(self.user_messages[message.author.id]) >= self.spam_threshold:
            if (current_time - self.user_messages[message.author.id][0]) <= self.time_interval:
                await self.handle_spam(message)

    async def handle_spam(self, message):
        try:
            await message.channel.send(f"{message.author.mention}, you are sending messages too quickly. Please slow down.")
            await message.author.timeout(duration=600)  # Timeout for 10 minutes (in seconds)
            await self.log_action(message, "Timeout")
        except discord.Forbidden:
            await message.channel.send("I do not have permission to timeout this user.")
        except Exception as e:
            await message.channel.send(f"An error occurred: {str(e)}")

    async def log_action(self, message, action):
        log_channel = discord.utils.get(message.guild.text_channels, name="mod-log")
        if log_channel:
            embed = discord.Embed(
                title="Anti-Spam Action",
                description=f"{message.author.mention} has been {action}.",
                color=discord.Color.red()
            )
            embed.add_field(name="Reason", value="Spam detection")
            embed.add_field(name="Channel", value=message.channel.mention)
            embed.add_field(name="Time", value=message.created_at.strftime("%Y-%m-%d %H:%M:%S"))
            await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AntiSpam(bot))
