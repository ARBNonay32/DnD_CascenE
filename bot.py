
import nest_asyncio
nest_asyncio.apply()

import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context
#import discord

from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='&')

<<<<<<< HEAD
@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{bot.user} is connected to the following guild: \n'
        f'{guild.name}(id: {guild.id})'
        )

=======
>>>>>>> af4fcdd6e6bb759692eae94151c6c974c36f12e1
@bot.command()
async def ping(ctx):
	await ctx.channel.send("pong")

@bot.command()
async def game_map(ctx, width: int, height: int):
    map = ""
    if ((width + 1) * height) > 1980:
        await ctx.channel.send("Given dimensions are too large, map area must be smaller than 1980 units")
    else:
        for i in range(height):
            for j in range(width):
                if j == 0 or j == width - 1:
                    map += "|"
                elif i == 0:
                    map += "‾‾"
                elif i == height - 1:
                    map += "__"
                else:
                    map += "  "
            map += "\n"
        await ctx.channel.send("```" + map + "```")



@bot.command()
async def print(ctx, arg):
	await ctx.channel.send(arg)

bot.run(TOKEN)