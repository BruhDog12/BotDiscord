import discord
from discord.ext import commands
from discord import FFmpegAudio
from discord.utils import get
from youtube_dl import YoutubeDL
import random

import datetime
import requests

from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('Token0')

bot = commands.Bot(command_prefix='',help_command=None) #prefix when you want to use the bot

@bot.event
async def on_ready(): #the bot send out to notify you when it works
    print(f"{bot.user} (Online Now)")

@bot.command(aliases=['user','info'])
@commands.has_permissions(kick_members=True)
async def whois(ctx, member : discord.Member):
    embed = discord.Embed(title = member.name , description = member.mention , color = 0x96679e)
    embed.add_field(name = 'ID', value = member.id ,inline=True)
    embed.set_thumbnail(url = member.avatar_url)
    embed.set_footer(icon_url=ctx.author.avatar_url, text = f"Requested by{ctx.author.name}")
    await ctx.channel.send(embed=embed)

images = ['https://media.npr.org/assets/img/2016/03/29/ap_090911089838_sq-3271237f28995f6530d9634ff27228cae88e3440.jpg',
          'https://i.pinimg.com/736x/b9/c3/22/b9c322032c499c81c92eea6704123253.jpg',
          'https://starecat.com/content/wp-content/uploads/sad-crying-dog-tears-reaction-meme.jpg',
          'https://img-9gag-fun.9cache.com/photo/a6E6A18_460s.jpg',
          'https://s.keepmeme.com/files/en_posts/20210107/girl-screaming-and-crying-meme.jpg',
          'https://siamblockchain.com/wp-content/uploads/2020/10/cat-crying-phone-meme.jpg',
          'https://s.keepmeme.com/files/en_posts/20200819/4fa40b57d8e0e0883eeff945503d94aecrying-cat-face-meme.jpg',
          'https://pbs.twimg.com/media/E0Oi7clXEAUO4MH.jpg']

@bot.command()
async def cry(ctx): #random some images for fun
    embed = discord.Embed(color = 0x96679e)
    random_link = random.choice(images)
    embed.set_image(url = random_link)
    await ctx.channel.send(embed=embed)

provinces = []
new_cases = []
@bot.command()
async def covid(ctx):
    embed = discord.Embed(title="Daily report each province", description="Report covid today", color = 0x96679e)
    CovidProvince = requests.get('https://covid19.ddc.moph.go.th/api/Cases/today-cases-by-provinces')
    Province1 = CovidProvince.json()
    for infected in Province1:
        x = (infected["province"])
        y = (infected["new_case"])
        provinces.append(x)
        new_cases.append(y)
        xx = "จังหวัด :"+str(x)
        yy = "จำนวนผู้ติดเชื้อ :"+str(y)
        embed.add_field(name= xx,value= yy,inline=False)
    currentDT = datetime.datetime.now()
    await ctx.channel.send(currentDT)
    embed.set_thumbnail(url='https://www.utc.ac.th/2020/wp-content/uploads/2020/04/tsct_eluf.jpg')
    embed.set_image(url="http://thg-health.com/images/2020/04/04/thonburihospital.jpg")
    embed.set_footer(icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Flag_of_Thailand_%28non-standard_colours%29.svg/1200px-Flag_of_Thailand_%28non-standard_colours%29.svg.png", 
    text = "Thailand")
    await ctx.channel.send(embed=embed)

@bot.command()
async def today(ctx):
    embed = discord.Embed(title="overall", description="Report covid today", color = 0x96679e)
    response = requests.get('https://covid19.ddc.moph.go.th/api/Cases/today-cases-all')
    data = response.json()[0]
    A=("ผุ้ติดเชื้อสะสม ")
    a1=data["total_case"]
    B=("ผู้ติดเชื้อใหม่วันนี้ ")
    b1=data["new_case"]
    C=("หายป่วยวันนี้ ")
    c1=data["new_recovered"]
    D=("เสียชีวิตวันนี้ ")
    d1=data["new_death"]
    E=("เสียชีวิตสะสม ")
    e1=data["total_death"]
    F=("หายป่วยสะสม ")
    f1=data["total_recovered"]
    embed.add_field(name=A,value=a1,inline=False)
    embed.add_field(name=B,value=b1,inline=False)
    embed.add_field(name=C,value=c1,inline=False)
    embed.add_field(name=D,value=d1,inline=False)
    embed.add_field(name=E,value=e1,inline=False)
    embed.add_field(name=F,value=f1,inline=False)
    embed.set_thumbnail(url='https://www.medicallinelab.co.th/wp-content/uploads/2021/10/omicron.jpg')
    embed.set_footer(icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Flag_of_Thailand_%28non-standard_colours%29.svg/1200px-Flag_of_Thailand_%28non-standard_colours%29.svg.png", 
    text = "Thailand")
    embed.set_image(url="https://binaries.templates.cdn.office.net/support/templates/en-us/lt89922682_quantized.png")
    await ctx.channel.send(embed=embed)

@bot.command() 
async def help(ctx): #Its like running a textbox
    embed = discord.Embed(title = "This is help for you Human!!", description = "All bot command", color = 0x96679e)
    embed.add_field(name="help", value = "Get help command.", inline = False)
    embed.add_field(name="covid",value = "For check to check the situation of covid in every provinces in TH.", inline = False)
    embed.add_field(name="today",value = "For check situation today.",inline=False)
    embed.add_field(name="play", value = "For play link from you tube.", inline = False)
    embed.add_field(name="cry", value = "For random some cry picture for fun.", inline = False)
    embed.add_field(name="pause",value = "For pause.")
    embed.add_field(name="resume",value = "For resume.")
    embed.add_field(name="stop",value = "For stop.")
    embed.add_field(name="leave",value = "For leave bot from channel.")
    embed.set_thumbnail(url='https://pbs.twimg.com/media/DgHtuapUwAAqmeR?format=jpg&name=small')
    await ctx.channel.send(embed=embed)

@bot.command()
async def play(ctx, url):
    channel = ctx.author.voice.channel
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client == None:
        await ctx.channel.send("join server")
        await channel.connect()
        voice_client = get(bot.voice_clients, guild=ctx.guild)
        
        YDL_OPTIONS = {'Format' : 'bestaudio','noplaylist' : 'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        
        if not voice_client.is_playing():
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                URL = info['formats'][0]['url']
                voice_client.play(discord.FFmpegPCMAudio(URL))
                voice_client.is_playing()
        else:
            await ctx.channel.send("Nope")
            return

@bot.command() #stop playing music
async def stop(ctx):
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client == None:
        await ctx.channel.send('No bot in channel')
        return
    if voice_client.channel != ctx.author.voice.channel:
        await ctx.channel.send("คุณไม่ได้อยุ่ห้องเดียวกับ{0}".format(voice_client.channel))
        return
    await ctx.channel.send("บอทหยุดเล่นเพลงแล้ว")
    voice_client.stop()

@bot.command() #pause bot
async def pause(ctx):
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client == None:
        await ctx.channel.send('No bot in channel')
        return
    if voice_client.channel != ctx.author.voice.channel:
        await ctx.channel.send("คุณไม่ได้อยุ่ห้องเดียวกับ{0}".format(voice_client.channel))
        return
    await ctx.channel.send("หยุดเเล้ว")
    voice_client.pause()

@bot.command() #resumed bot
async def resumed(ctx):
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client == None:
        await ctx.channel.send('No bot in channel')
        return
    if voice_client.channel != ctx.author.voice.channel:
        await ctx.channel.send("คุณไม่ได้อยุ่ห้องเดียวกับ{0}".format(voice_client.channel))
        return
    await ctx.channel.send("ดำเนินต่อ")
    voice_client.resumed()

@bot.command() #leave bot from channel
async def leave(ctx):
    await ctx.voice_client.disconnect()
    await ctx.channel.send("เอาบอทออกเเล้ว")

@bot.event
async def on_message(message): #Using a bot to reply to messages
    await bot.process_commands(message)

bot.run(token)
