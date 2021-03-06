# -*- coding: utf-8 -*-


import nest_asyncio
nest_asyncio.apply()

import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context
#import discord

from discord.ext import commands
import cv2
from dotenv import load_dotenv
import discord

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='&')

players = []
gmap = ""
oldgmap = ""
gwidth = 0
gheight = 0

@bot.command()
async def ping(ctx):
    await ctx.channel.send("pong")

@bot.command()
async def game_map(ctx, width: int, height: int):

    global gwidth
    global gheight
    global gmap

    gwidth = width*2 + 1
    gheight = height*2 + 1

    gmap = "";
    if width > 70:
        temp = height
        height = width
        width = temp

    if ((width + 1) * height) > 1980:
        await ctx.channel.send("Given dimensions are too large, map area must be smaller than 1980 units")

    else:
        width = width*2
        for i in range(height):
            for j in range(width):
                if j == 0 or j == width - 1:
                    gmap += "|"
                elif i == 0:
                    gmap += "‾"
                elif i == height - 1:
                    gmap += "_"
                else:
                    gmap += " "
            gmap += "\n"
        await ctx.channel.send("```" + gmap + "```")


@bot.command()
async def build(ctx, tlx: int, tly: int, brx: int, bry: int):

    global gwidth
    global gheight
    global gmap
    global oldgmap

    chArray = list(gmap)

    if tlx>brx:
        temp = tlx
        tlx = brx
        brx = temp

    if tly>bry:
        temp = tly
        tly = bry
        bry = temp

    oldgmap = gmap

    for k in range(abs(tly - bry)):
        for l in range(abs(tlx - brx)*2):
            if l == 0 or l == abs(tlx - brx)*2 - 1:
                chArray[((tly + k)*gwidth + l + tlx*2)] = "‖"
            elif k == abs(tly - bry) - 1:
                chArray[((tly + k)*gwidth + l + tlx*2)] = "‗"
            elif k == 0:
                chArray[((tly + k)*gwidth + l + tlx*2)] = "˭"

            #await ctx.channel.send(str((tly + k)*gwidth) + " " + str(l) + " " + str(tlx))

    gmap = "".join(chArray)

    await ctx.channel.send("```" + gmap + "```")


@bot.command()
async def build_spec(ctx, tlx: int, tly: int, brx: int, bry: int, char: str):

    global gwidth
    global gheight
    global gmap
    global oldgmap

    chArray = list(gmap)

    if tlx>brx:
        temp = tlx
        tlx = brx
        brx = temp

    if tly>bry:
        temp = tly
        tly = bry
        bry = temp

    oldgmap = gmap

    for k in range(abs(tly - bry)):
        for l in range(abs(tlx - brx)*2):
            if l == 0 or l == abs(tlx - brx)*2 - 1:
                chArray[((tly + k)*gwidth + l + tlx*2 + 1)] = char
            elif k == abs(tly - bry) - 1:
                chArray[((tly + k)*gwidth + l + tlx*2 + 1)] = char
            elif k == 0:
                chArray[((tly + k)*gwidth + l + tlx*2 + 1)] = char

            #await ctx.channel.send(str((tly + k)*gwidth) + " " + str(l) + " " + str(tlx))

    gmap = "".join(chArray)

    await ctx.channel.send("```" + gmap + "```")

@bot.command()
async def save_as(ctx, filename: str):
	try:
		global gmap
		global gwidth
		global gheight
		f = open("_".join(["userFile",filename]), "w", encoding="utf-8")
		f.write("\t".join([str(gwidth), str(gheight), gmap]))
		f.close()
		await ctx.channel.send("```File Written```")
	except Exception as e:
		await ctx.channel.send(f"```Error when writing file '{filename}' with the following error:\n {str(e)}"[0:1996]+"```")

@bot.command()
async def load_map(ctx, filename: str):
	try:
		global gmap
		global gwidth
		global gheight
		f = open("_".join(["userFile",filename]), "r", encoding="utf-8")
		temp = f.read()
		tgwidth, tgheight, gmap = temp.split("\t")
		gwidth = int(tgwidth)
		gheight = int(tgheight)
		await ctx.channel.send("```" + gmap + "```")
	except Exception as e:
		await ctx.channel.send(f"```Error when reading file '{filename}':\n {str(e)}"[0:1996]+"```")



@bot.command()
async def listplayers(ctx):
    for player in players:
        await ctx.channel.send(player[0])

@bot.command()
async def print(ctx, arg):
    await ctx.channel.send(arg)

@bot.command()
async def add_player(ctx, name, xpos: int, ypos: int):
    global players
    global gmap
    global gwidth
    global gheight
    global oldgmap

    oldgmap = gmap
    xpos = xpos*2
    valid = True
    if xpos < 0 or xpos > gwidth - 1 or ypos < 0 or ypos > gheight - 1:
        await ctx.channel.send("Your character would be out of bounds at these coordinates")
        valid = False
    listMap = list(gmap)
    if listMap[ypos * gwidth + xpos] != " ":
        await ctx.channel.send("Your character would be inside a wall or something at these coordinates")
        valid = False
    if len(name) > 1:
        listMap[ypos * gwidth + xpos] = name[0]
    else:
        listMap[ypos * gwidth + xpos] = name
    if valid:
        players.append((name, xpos, ypos))
        gmap = "".join(listMap)
        await ctx.channel.send("```" + gmap + "```")

@bot.command()
async def move(ctx, name, newx: int, newy: int):

    newx = newx*2
    global gmap
    global oldgmap
    listMap = list(gmap)
    old = None
    oldgmap = gmap
    valid = True
    if newx < 0 or newx > gwidth - 1 or newy < 0 or newy > gheight - 1:
        await ctx.channel.send("Your character would be out of bounds at these coordinates")
        valid = False
    if listMap[newy * gwidth + newx] != " ":
        await ctx.channel.send("Your character would be inside a wall or something at these coordinates")
        valid = False

    for player in players:
        if player[0] == name:
            old = player
            players.remove(old)
    if old == None:
        await ctx.channel.send("This player does not exist. Check your spelling or use &listplayers.")
        return

    listMap[old[2] * gwidth + old[1]] = " "
    if len(name) > 1:
        listMap[newy * gwidth + newx] = name[0]
    else:
        listMap[newy * gwidth + newx] = name
    if valid:
        players.append((name, newx, newy))
        gmap = "".join(listMap)
        await ctx.channel.send("```" + gmap + "```")


@bot.command()
async def line(ctx, x0: int, y0: int, x1: int, y1: int, char: str):

    global gwidth
    global gheight
    global gmap
    global oldgmap


    #start
    oldgmap = gmap
    points = [];
    dx = x1 - x0
    dy = y1 - y0
    N =  max(abs(dx), abs(dy)*2);   #may move *2 to l in points loop

    for step in range(N+1):

        t = 0
        if (N == 0):
            t = 0.0
        else:
            t = step / N

        vx = round(x0 + t * dx)
        vy = round(y0 + t * dy)

        pxy = (vx, vy)

        points.append(pxy)


    chArray = list(gmap)


    for pr in points:
        chArray[(pr[1]*gwidth + pr[0]*2 + 1)] = char

    gmap = "".join(chArray)

    await ctx.channel.send("```" + gmap + "```")


@bot.command()
async def picture(ctx, pip_w: int, pip_h: int):

    background = cv2.imread('picture1.png')
    overlay = cv2.imread('lucas.png')

    wb, hb, ht = background.shape
    w, h, t = overlay.shape

    resized_image = cv2.resize(overlay, (h//10, w//10))
    h1, w1 = resized_image.shape[:2]

    background[pip_h:pip_h+h1,pip_w:pip_w+w1] = resized_image  # make it PIP

    cv2.imwrite('combined.png', background)

    await ctx.channel.send(file=discord.File('combined.png'))


@bot.command()
async def repeat(ctx, arg):
	await ctx.channel.send(arg)

@bot.command()
async def undo(ctx):
    global gmap
    global oldgmap
    gmap = oldgmap
    await ctx.channel.send("```" + gmap + "```")

bot.run(TOKEN)
