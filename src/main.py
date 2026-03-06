import os
from discord import Intents
from bot import Bot
from dotenv import load_dotenv
from discord import app_commands
import discord

intents = Intents.default()
intents.message_content = True
bot = Bot('', help_command = None, intents = intents)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Sync cogs and cog commands, run once at setup
@bot.event
async def setup_hook():
    guild = discord.Object(id = '520337076659421192')

    for filename in os.listdir("src/controller"):
        if filename.endswith(".py"):
            await bot.load_extension(f"controller.{filename[:-3]}")
    
    synced = await bot.tree.sync()
    guild_synced = await bot.tree.sync(guild = guild)
    print(f"Synced {len(synced)} commands(s)")
    print(f"Synced {len(guild_synced)} guild commands(s)")

@bot.tree.command(name = "ping", description = "Check bot ping")
async def ping(ctx):
    await ctx.response.send_message(content = f"Pong! {round(bot.latency * 1000, 1)}ms")

if __name__ == "__main__":
    bot.run(f"{BOT_TOKEN}")