import discord
import random
import numpy
from discord.ext import commands

TOKEN = 'NzEzMDk4NzYzNzg2MjU2NDM0.XsbLAw.Y97QUk-R9TbutrbWkoYcZn5XLq8'
botprefix = '!'

bot = commands.Bot(botprefix)

async def process_command(message):
    input_split = message.content[len(botprefix):].split()

    #no commands
    if len(input_split) == 0:
        await message.channel.send("Don't know this command!")
        return

    cmd = input_split[0]
    modifiers = input_split[1:]

    if cmd.lower() == 'hello':
        await message.channel.send("Hello!")

    elif cmd == 'getnum':
        if len(bot.number_pool) != 0:
            num = bot.number_pool.pop()
            await message.author.send("Your secret number is: " + str(num))
        else:
            await message.author.send("Out of numbers!")

    elif cmd == 'rnum':
        rnum = len(bot.number_pool)
        await message.channel.send("Remaining number of numbers: " + str(rnum))

    elif cmd == 'reset':
        if len(input_split) < 2:
            await message.channel.send("Incomplete command! Usage: !reset <max int>")
            return
        arg = int(modifiers[0])
        if type(arg) == int and arg > 0:
            bot.number_pool = list(range(arg))
            random.shuffle(bot.number_pool)
            await message.channel.send("Reset!")
        else:
            await message.channel.send("Incomplete command!")

    #invalid command
    else:
        await message.channel.send("Don't know this command!")

@bot.event
async def on_connect():
    bot.number_pool = list(range(5))
    random.shuffle(bot.number_pool)
    print("dndbot ready!")

@bot.event
async def on_message(message):
    if message.author == bot.user: #don't respond to itself
        return
    if message.content.startswith(botprefix):
        await process_command(message)

bot.run(TOKEN)