import discord
from discord.ext import commands
from discord import FFmpegAudio
from discord.utils import get
from youtube_dl import YoutubeDL
import random

from dotenv import load_dotenv
import os

from covid import covidtoday
from covid import keep_value

load_dotenv()
token = os.getenv('Token0')

bot = commands.Bot(command_prefix='',help_command=None) #prefix when you want to use the bot

@bot.event
async def on_ready(): #the bot send out to notify you when it works
    print(f"{bot.user} (Online Now)")

@bot.command(aliases=['user','info'])
@commands.has_permissions(kick_members=True)
async def whois(ctx, member : discord.Member):
    embed = discord.Embed(title = member.name , describtion = member.mention , color = 0x96679e)
    embed.add_field(name = 'ID', value = member.id ,inline=True)
    embed.set_thumbnail(url = member.avatar_url)
    embed.set_footer(icon_url=ctx.author.avatar_url, text = f"Requested by{ctx.author.name}")
    await ctx.channel.send(embed=embed)

images = ['https://i.pinimg.com/550x/ea/bc/2c/eabc2cc1fb21eb8ae6cdd37ebab52fb5.jpgv',
          'https://i.pinimg.com/736x/b9/c3/22/b9c322032c499c81c92eea6704123253.jpg',
          'https://c.tenor.com/BiSnYM1CZq8AAAAd/crying-cry.gif',
          'data:image/jpeg;base64,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',
          'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRyYc14tGSN9TX_-lAywSyhUDYi7DEmKwuj8w&usqp=CAU',
          'https://siamblockchain.com/wp-content/uploads/2020/10/cat-crying-phone-meme.jpg']

@bot.command()
async def cry(ctx):
    embed = discord.Embed(color = 0x96679e)
    random_link = random.choice(images)
    embed.set_image(url = random_link)
    await ctx.channel.send(embed=embed)

@bot.command()
async def covid(ctx):
    embed = discord.Embed(title="Daily report", describe="Report covid today", color = 0x96679e)
    embed.add_field(name= "province",)

    await ctx.channel.send(embed=embed)

@bot.command() 
async def help(ctx): #Its like running a textbox
    embed = discord.Embed(title = "This is help for you Human!!", descrition = "All bot command", color = 0x96679e)
    embed.add_field(name="help", value = "Get help command.", inline = False)
    embed.add_field(name="play", value = "pause,resume,stop,leave", inline = False)
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
            await ctx.channel.send("kuy")
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
    await ctx.send.channel("เอาบอทออกเเล้ว")

@bot.event
async def on_message(message): #Using a bot to reply to messages
    await bot.process_commands(message)

bot.run(token)