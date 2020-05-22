import discord
import random
from discord.ext import commands

TOKEN = ''
botprefix = '!'

bot = commands.Bot(botprefix)

async def process_command(message):
    cmd = message.content[len(botprefix):].split()

    #no commands
    if len(cmd) == 0:
        await message.channel.send("Don't know this command!")
        return


    if cmd[0] == 'Hello':
        await message.channel.send("Hello!")

    elif cmd[0] == 'getnum':
        if len(bot.number_pool) != 0:
            num = bot.number_pool.pop()
            await message.author.send("Your secret number is: " + str(num))
        else:
            await message.author.send("Out of numbers!")

    elif cmd[0] == 'rnum':
        rnum = len(bot.number_pool)
        await message.channel.send("Remaining number of numbers: " + str(rnum))

    elif cmd[0] == 'reset':
        if len(cmd) < 2:
            await message.channel.send("Incomplete command! Usage: !reset <max int>")
            return
        arg = int(cmd[1])
        if type(arg) == int and arg > 0:
            bot.number_pool = list(range(arg))
            random.shuffle(bot.number_pool)
            await message.channel.send("Reset!")
        else:
            await message.channel.send("Incomplete command!")

    else:
        await message.channel.send("Don't know this command!")

@bot.event
async def on_connect():
    bot.number_pool = list(range(5))
    random.shuffle(bot.number_pool)
    print("bot ready!")

@bot.event
async def on_message(message):
    if message.author == bot.user: #don't respond to itself
        return
    if message.content.startswith(botprefix):
        await process_command(message)

bot.run(TOKEN)