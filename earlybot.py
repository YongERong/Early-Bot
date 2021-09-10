from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import discord
from discord.ext import commands
import requests
import re
import os
from dotenv import load_dotenv

load_dotenv()
#headless, disable extensions, disable gpu, disable images
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")
chrome_options.add_argument('--blink-settings=imagesEnabled=false')
chrome_options.binary_location = os.environ['GOOGLE_CHROME_BIN']
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.add_argument('--no-sandbox')

#on startup
activity = discord.Activity(type=discord.ActivityType.watching, name="?help")
driver = webdriver.Chrome(os.environ['CHROMEDRIVER_PATH'], options=chrome_options)
bot = commands.Bot(command_prefix="?", activity=activity ,help_command=None)

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
    url = "https://www.nike.com/" + arg1 + "/launch/t/" + arg2.replace(" ", "-")
    driver.get(url)
    #Grab all items from network tab of google chrome developer tools into a list of dictionaries
    data = driver.execute_script("var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;")
    #Get the name of every dictionary within the list of dictionary in a list
    names = [obj['name'] for obj in data]
    #Product id links
    ilinks = [name for name in names if name.startswith("https://api.nike.com/merch/skus/v2/?filter=productId%")]
    ilinks = list(set(ilinks))
    print(ilinks)
    for links in ilinks:
        a = requests.get(links)
        subsizes = [size.split('"')[2] for size in re.findall(r'nikeSize" : "\S{1,4}',a.text,re.ASCII)]
        print(subsizes)
        if arg3 in subsizes:
            id = links.removeprefix("https://api.nike.com/merch/skus/v2/?filter=productId%28")
            id = id.split("%",1)[0]
            break
    try:
        elink = url + "?productId=" + id + "&size=" + arg3     
    except(UnboundLocalError):
        await ctx.channel.send("No product with matching name and size is found in that region")
        raise
    await ctx.channel.send(elink)

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency*1000)}ms")

@bot.command()
async def help(ctx):
    embed=discord.Embed(title="Early Bot Help", description="Version 1.0.0", color = discord.Colour.random())
    embed.add_field(name="```?snkrs <Region> <Name in quotes or with dashes> < US size>```",value="Command for Nike SNKRS early link, size chart can be found [here](https://www.nike.com/sg/size-fit/mens-footwear)",inline=False)
    embed.add_field(name="```?ping```",value="Check if the bot is online",inline=False)
    await ctx.send(embed=embed)

bot.run(os.environ['TOKEN'])