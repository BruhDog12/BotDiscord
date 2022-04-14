import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='',help_command=None)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def test(ctx, *, par):
    await ctx.channel.send("You typed {0}".format(par))

@bot.command()
async def help(ctx):
    emBed = discord.Embed(title="Tutorial", descrition="All bot command", color=0x96679e)
    emBed.add_field(name="help", value="Get help command", inline=True)
    await ctx.channel.send(embed=emBed)

@bot.event
async def on_message(message):
    if message.content == "How to":
        print(message.channel)
        await message.channel.send("พิมพ์ P เพื่อเปิดเพลง")
    elif message.content == "out":
        await bot.logout()
    await bot.process_commands(message)

bot.run('')