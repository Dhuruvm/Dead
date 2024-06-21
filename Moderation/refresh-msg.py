import discord
from discord.ext import commands
import asyncio

class RefreshMessages(commands.Cog):
    def __init__(self, bot, channel_id):
        self.bot = bot
        self.channel_id = channel_id

    @commands.Cog.listener()
    async def on_ready(self):
        print('RefreshMessages cog loaded')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id != self.channel_id:
            return

        # Check if the message is from the bot
        if message.author == self.bot.user:
            await asyncio.sleep(3)
            try:
                await message.delete()
            except discord.NotFound:
                pass
            except discord.Forbidden:
                print(f"Failed to delete bot message in {message.channel.name} due to lack of permissions.")

async def setup(bot):
    channel_id = 1196828527127973990  # Replace with your channel ID
    await bot.add_cog(RefreshMessages(bot, channel_id))
