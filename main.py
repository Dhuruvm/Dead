import discord
from discord.ext import commands
import os
import json
import asyncio
import time

# Load config file
with open('config.json') as config_file:
    config = json.load(config_file)

intents = discord.Intents.all()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=config['command_prefix'], intents=intents)

# Cooldowns dictionary
# {command_name: CooldownMapping}
cooldowns = {}

async def load_extensions():
    # Helper function to load a single extension with retry on rate limit
    async def load_extension_with_retry(extension_name):
        try:
            await bot.load_extension(extension_name)
            print(f"Loaded extension: {extension_name}")
        except discord.errors.HTTPException as e:
            if e.status == 429:
                retry_after = int(e.response.headers.get("Retry-After", 2))
                print(f"Rate limited. Retrying {extension_name} after {retry_after} seconds...")
                await asyncio.sleep(retry_after)
                await load_extension_with_retry(extension_name)
            else:
                print(f"Failed to load extension {extension_name}: {e}")

    # Load extensions from the Moderation folder
    for filename in os.listdir('./Moderation'):
        if filename.endswith('.py'):
            await load_extension_with_retry(f'Moderation.{filename[:-3]}')

    # Load extensions from the Modals folder
    for filename in os.listdir('./modals'):
        if filename.endswith('.py'):
            await load_extension_with_retry(f'modals.{filename[:-3]}')

    # Load extensions from the Guide folder
    for filename in os.listdir('./Guide'):
        if filename.endswith('.py'):
            await load_extension_with_retry(f'Guide.{filename[:-3]}')

    # Load extensions from the events folder
    for filename in os.listdir('./events'):
        if filename.endswith('.py'):
            await load_extension_with_retry(f'events.{filename[:-3]}')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(config['bot_token'])

asyncio.run(main())
