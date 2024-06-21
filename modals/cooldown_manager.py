import discord
from discord.ext import commands
from collections import defaultdict
import time

class CooldownManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldowns = defaultdict(dict)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cooldown cog loaded')

    def check_cooldown(self, user_id: int, command_name: str, cooldown: int) -> bool:
        current_time = time.time()
        if user_id in self.cooldowns[command_name]:
            last_time = self.cooldowns[command_name][user_id]
            if current_time - last_time < cooldown:
                return False
        self.cooldowns[command_name][user_id] = current_time
        return True

# The setup function is async, and it should take bot as a parameter

async def setup(bot):
 await bot.add_cog(CooldownManager(bot))
