import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import os

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

# Folders to search for cog files (Python modules) to auto-load
# Add or remove folder names here, e.g.: ["cogs", "another_cog_folder"]
COG_FOLDERS = [
    "cogs",
    "events",
]

class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None
        )
    
    async def setup_hook(self):
        """Load cogs when bot starts"""
        base_dir = os.path.dirname(os.path.abspath(__file__))

        for folder in COG_FOLDERS:
            folder_path = os.path.join(base_dir, folder)

            if not os.path.isdir(folder_path):
                print(f"[WARN] Cog folder not found: {folder_path}")
                continue

            for filename in os.listdir(folder_path):
                if not filename.endswith(".py") or filename.startswith("__"):
                    continue

                module_name = filename[:-3]  # strip .py

                # Python modules can't have spaces or invalid characters
                if " " in module_name:
                    print(f"[SKIP] Invalid cog filename (contains spaces): {filename}")
                    continue

                ext_path = f"{folder}.{module_name}"

                try:
                    await self.load_extension(ext_path)
                    print(f"[COG] Loaded {ext_path}")
                except Exception as e:
                    print(f"[COG] Failed to load {ext_path}: {e}")
        
        # Sync commands
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(f"Failed to sync commands: {e}")
    
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        print(f'Bot is in {len(self.guilds)} guilds')

# Create bot instance
bot = DiscordBot()

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    
    # Read token from environment variable DISCORD_TOKEN
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        raise RuntimeError('DISCORD_TOKEN environment variable is not set')

    try:
        bot.run(token)
    except Exception as e:
        print(f"[ERROR] Bot crashed: {e}")
        import traceback
        traceback.print_exc()
