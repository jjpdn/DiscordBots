import discord
import random

TOKEN = 'NzA1MTUwOTI5MzM4NjMwMTY1.XqnhZg.R5LeoaNJ54PpxUo0IlImMOBglWo'

botprefix = '!'

number_pool = list(range(5))
random.shuffle(number_pool)

async def process_command(message):
    cmd = message.content[len(botprefix):].split()

    if len(cmd) == 0:
        await message.channel.send("Don't know this command!")
        return

    if cmd[0] == 'Hello':
        await message.channel.send("Hello!")
    elif cmd[0] == 'getnum':
        if len(number_pool) != 0:
            num = number_pool.pop()
            await message.author.send("Your secret number is: " + str(num))
        else:
            await message.author.send("Out of numbers!")
    elif cmd[0] == 'rnum':
        rnum = len(number_pool)
        await message.channel.send("Remaining number of numbers: " + str(rnum))
    else:
        await message.channel.send("Don't know this command!")


client = discord.Client()

@client.event
async def on_connect():
    #number_pool = random.shuffle(list(range(5)))
    print("bot ready!")

@client.event
async def on_message(message):
    if message.author == client.user: #don't respond to itself
        return
    if message.content.startswith(botprefix):
        await process_command(message)

client.run(TOKEN)