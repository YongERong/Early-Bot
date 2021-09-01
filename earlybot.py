from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import discord
from discord.ext import commands
import requests
import re
import os
from time import perf_counter #log
#import aiohttp

#headless, disable extensions, disable gpu, disable images
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")
chrome_options.add_argument('--blink-settings=imagesEnabled=false')

#on startup
driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=chrome_options)
bot = commands.Bot(command_prefix="?", help_command=None, description="""Listening on ?help
Developed by @noone""")


#remove token later
bot.run(os.environ['TOKEN'])


@bot.command()
async def snkrs(ctx:str, arg1:str, arg2:str, arg3:str):
    start = perf_counter() #log
    if len(arg1) != 2 or arg1.isascii() == False:
        await ctx.channel.send("Region is incorrect")
        raise
    if len(arg2) < 5 or len(arg2) > 60 or arg2.isascii() == False:
        await ctx.channel.send("Name is incorrect")
        raise
    if len(arg3) < 1 or len(arg3) > 4 or arg3.isascii() == False:
        await ctx.channel.send("Size is incorrect")
        raise
    stop_errorcheck = perf_counter() #log
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
    stop_selscrape = perf_counter() #log
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
        await ctx.channel.send("Size requested is not compatible with product")
        raise
    stop_apiscrape = perf_counter() #log
    await ctx.channel.send(elink)
    #log
    await ctx.channel.send("""
    Total time taken: {}s
    Time taken for error prevention: {}s
    Time taken for Selenium scrape: {}s
    Time taken for api scrape: {}s""".format(stop_apiscrape - start, stop_errorcheck - start, stop_selscrape - stop_errorcheck, stop_apiscrape - stop_selscrape))

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency*1000)}ms")

@bot.command()
async def help(ctx):
    embed=discord.Embed(title="Early Bot Help", description="Version 0.3.0", color = discord.Colour.random())
    embed.add_field(name="```?snkrs <Region> <name in quotes or with dashes> <size>```",value="Command for Nike SNKRS early link",inline=False)
    embed.add_field(name="```?ping```",value="Check if the bot is online",inline=False)
    await ctx.send(embed=embed)








