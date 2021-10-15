import discord
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv

load_dotenv()

#on startup
activity = discord.Activity(type=discord.ActivityType.watching, name="?help")
bot = commands.Bot(command_prefix="?", activity=activity ,help_command=None)
header = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"}
reqSession = requests.Session()

@bot.command()
async def snkrs(ctx:str, arg1:str, arg2:str, arg3:str):
    if len(arg1) != 2 or arg1.isascii() == False:
        await ctx.channel.send("Region is incorrect")
        raise
    if len(arg2) < 5 or len(arg2) > 60 or arg2.isascii() == False:
        await ctx.channel.send("Name is incorrect")
        raise
    if len(arg3) < 1 or len(arg3) > 4 or arg3.isascii() == False:
        await ctx.channel.send("Size is incorrect")
        raise
    if arg1 != "us":
        url = "https://www.nike.com/" + arg1 + "/launch/t/" + arg2.replace(" ", "-")
    else:
        url = "https://www.nike.com/launch/t/" + arg2.replace(" ","-")
    page = reqSession.get(url, headers=header)

    try:
        #Log title
        title = page.text.split("</title>")[0].split('<title data-react-helmet="true">')[1]
        print(title)
        #try to obtain arrays of sizes and ids
        workingText = page.text.split('"skus"')[1].split('"merchProductStatus"')[0]
        sizeList = [size[0:4].split('"')[0] for size in workingText.split('"nikeSize":"')[1:]]
        print(sizeList)
        idList = [id[0:35] for id in workingText.split('"productId":"')[1:]]
        print(idList)
        reqSession.cookies.clear()
        #try to form the early link
        id = idList[sizeList.index(arg3)]
        elink = url + "?productId=" + id + "&size=" + arg3   
    #If index error due to lack of "skus" in webpage or unable to find matching size and product value
    except(UnboundLocalError,ValueError,IndexError):
        await ctx.channel.send("No product with matching name and size is found in that region")
        raise
    await ctx.channel.send(elink)

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency*1000)}ms")

@bot.command()
async def help(ctx):
    embed=discord.Embed(title="Early Bot Help", description="Version 2.0.0", color = discord.Colour.from_rgb(255,255,255))
    embed.add_field(name="```?snkrs <Region> <Product name with dashes> < US size>```",value="\nE.g. Link to the product is: ```https://www.nike.com/sg/launch/t/air-jordan-1-pollen``` and you want US size 9. The command will be: ```?snkrs sg air-jordan-pollen 9```\nCommand for Nike SNKRS early link, size chart can be found [here](https://www.nike.com/sg/size-fit/mens-footwear)",inline=False)
    embed.add_field(name="```?ping```",value="Check if the bot is online",inline=False)
    await ctx.send(embed=embed)

bot.run(os.environ['TOKEN'])