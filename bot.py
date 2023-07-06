import discord, asyncio, os, dotenv

from discord.ext import commands, tasks
from itertools import cycle

# Load .env
dotenv.load_dotenv()
discord_token = os.getenv('token')

# Call all intents
intents = discord.Intents.all()

# Call certain intents
intents.members = True

# Set prefix and intents
client =commands.Bot(command_prefix="s!", intents=intents)

# Make a looping bot status
bot_status = cycle([
    "Testing",
    "example"
])

# Remove defualt help command
client.remove_command('help')

# Loop status
@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(bot_status)))

# on_ready event
@client.event
async def on_ready():
    try: 
        # Sync slash commands
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} commands!")
    except:
        print('already synced')

    change_status.start() # Start status
    print(f"Sucessfully logged in as {client.user}")

# First Slash Command
@client.tree.command(name='ping', description='Simple ping command')
async def roulette(interaction: discord.Interaction):
    embed = discord.Embed(title='Pong!', color=0xFD7720)
    await interaction.response.send_message(embed=embed)

# Run bot
async def main():
    async with client:
        await client.start(discord_token)

asyncio.run(main())
