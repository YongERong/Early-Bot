from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import discord
from discord.ext import commands
import requests
import re

#headless, disable extensions, disable gpu, disable images
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")
chrome_options.add_argument('--blink-settings=imagesEnabled=false')

#on startup
driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=chrome_options)

# Discord
bot = commands.Bot(command_prefix="?", help_command=None, description="""Listening on ?help
Developed by @noone""")


@bot.command()
async def snkrs(ctx:str, arg1:str, arg2:str, arg3:str):
    if len(arg1) != 2:
        await ctx.channel.send("Region is incorrect")
        raise
    if len(arg2) < 5 or len(arg2) > 60:
        await ctx.channel.send("Name is incorrect")
        raise
    if len(arg3) < 1 or len(arg3) > 4:
        await ctx.channel.send("Size is incorrect")
        raise



    url = "https://www.nike.com/" + arg1 + "/launch/t/" + arg2.replace(" ", "-")
    print(url)
    driver.get(url)

    #Grab all items from network tab of google chrome developer tools into a list of dictionaries
    data = driver.execute_script("var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;")
    #Get the name of every dictionary within the list of dictionary in a list
    names = [obj['name'] for obj in data]
    #Product id links
    ilinks = [name for name in names if name.startswith("https://api.nike.com/merch/skus/v2/?filter=productId%")]
    print(ilinks)
    #Product ids and remove duplicates
    ids = [link.removeprefix("https://api.nike.com/merch/skus/v2/?filter=productId%28") for link in ilinks]
    ids = [link2.split("%",1)[0] for link2 in ids]
    ids = list(set(ids))
    print(ids)
    if len(ids) != 1:
        ids = []
        sizes = []
        for links in ilinks:
            a = requests.get(links)
            #b = ast.literal_eval(a.text)
            #subids = [e.get('productId') for c in b for d in c for e in d]
            #subsizes = [e.get('nikeSize') for c in b for d in c for e in d]
            #subids = re.findall(r'productId" : "\w{8}-\w{4}-\w{4}-\w{4}-\w{12}',a.text,re.ASCII)
            subsizes = [size.split('"')[2] for size in re.findall(r'nikeSize" : "\S{1,4}',a.text,re.ASCII)]
            #print(subids)
            print(subsizes)
            #ids.append(subids)
            #sizes.append(subsizes)
            if arg3 in subsizes:
                id = links.removeprefix("https://api.nike.com/merch/skus/v2/?filter=productId%28")
                id = id.split("%",1)[0]
                print(id)
                break

        #print(ids)
        #print(sizes)
        #id = ids[sizes.index(arg3)]
    else:
        id = ids[0]

    elink = url + "?productId=" + id + "&size=" + arg3
        
        
                
    await ctx.channel.send(elink)

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency*1000)}ms")

@bot.command()
async def help(ctx):
    embed=discord.Embed(title="Early Bot Help", description="Version 0.1.0", color = discord.Colour.random())
    embed.add_field(name="```?snkrs <Region> <name in quotes or with dashes> <size>```",value="Command for Nike SNKRS early link",inline=False)
    embed.add_field(name="```?ping```",value="Check if the bot is online",inline=False)
    await ctx.send(embed=embed)


  


#remove token later
bot.run("ODgxNTUxNzM0Nzg1MzIzMDM4.YSufCA.ftsBX1KZ0BiSpFBGNm1AqPLl1WM")






