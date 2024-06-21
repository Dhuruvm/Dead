import discord
from discord.ext import commands
from datetime import datetime

class AFK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.afk_users = {}  # Dictionary to store AFK statuses
        self.bot.add_listener(self.on_message, "on_message")

    @commands.Cog.listener()
    async def on_ready(self):
        print('afk cog loaded')

    @commands.command()
    async def afk(self, ctx, *, message="I am currently AFK"):
        """Set your AFK status with an optional message"""
        if ctx.author.id in self.afk_users:
            # User is already AFK, update message if necessary
            if self.afk_users[ctx.author.id]["message"] == message:
                await ctx.send("")
            else:
                self.afk_users[ctx.author.id]["message"] = message
                await ctx.send("Your AFK status message has been updated.")
        else:
            # User is not AFK, set AFK status
            self.afk_users[ctx.author.id] = {"message": message, "time": datetime.now()}
            embed = discord.Embed(
                title="AFK Status",
                description=f"{ctx.author.mention} is now AFK",
                color=discord.Color.blue()
            )
            embed.add_field(name="Reason", value=message)
            embed.set_footer(text="You will be marked as AFK until you send another message.")
            await ctx.send(embed=embed)

    async def on_message(self, message):
        # Check if the message is from a bot to avoid loops
        if message.author.bot:
            return

        if message.content.startswith('?afk'):
            return  # Ignore ?afk command messages to avoid duplicate embeds

        mentioned_afk = []  # List to store AFK notices for multiple mentions

        for mentioned_user in message.mentions:
            if mentioned_user.id in self.afk_users:
                afk_info = self.afk_users[mentioned_user.id]
                afk_message = afk_info["message"]
                embed = discord.Embed(
                    title="AFK Notice",
                    description=f"{mentioned_user.mention} is AFK",
                    color=discord.Color.orange()
                )
                embed.add_field(name="Reason", value=afk_message)
                embed.add_field(name="AFK since", value=afk_info["time"].strftime("%Y-%m-%d %H:%M:%S"))
                mentioned_afk.append(embed)  # Append each AFK embed to the list

        if mentioned_afk:
            await message.channel.send(embed=mentioned_afk[0])  # Send only the first AFK notice

        # Check if the author of the message was AFK and remove the AFK status
        if message.author.id in self.afk_users:
            afk_info = self.afk_users.pop(message.author.id)
            afk_time = afk_info["time"]
            duration = datetime.now() - afk_time
            minutes, seconds = divmod(duration.total_seconds(), 60)
            hours, minutes = divmod(minutes, 60)
            days, hours = divmod(hours, 24)
            afk_duration = f"{int(days)} days, {int(hours)} hours, {int(minutes)} minutes"
            embed = discord.Embed(
                title="Welcome Back!",
                description=f"Welcome back {message.author.mention}",
                color=discord.Color.green()
            )
            embed.add_field(name="AFK Duration", value=afk_duration)
            embed.set_footer(text="Your AFK status has been removed.")
            await message.channel.send(embed=embed)

        await self.bot.process_commands(message)  # Ensure other commands still work

async def setup(bot):
    await bot.add_cog(AFK(bot))
