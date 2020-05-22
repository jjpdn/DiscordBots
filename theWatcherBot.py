import random
import os.path
import jsonpickle
from discord.ext import commands


class Data(object):
    def __init__(self):
        self.main_channel = "test"
        self.player_roles = []
        self.initialized = 0



# --------------- BOT SETUP ------------------

token_file = open("data/watchertoken", "r")
TOKEN = token_file.read()
data_path = "data/watcherdata.json"
botprefix = '!'

bot = commands.Bot(botprefix)

@bot.event
async def on_connect():
    # variables
    bot.number_pool = list(range(5))
    random.shuffle(bot.number_pool)
    # read saves
    file = open(data_path)
    if (os.path.isfile(data_path)):
        bot.data = jsonpickle.decode(file.read())
        print("loaded old save")
    else:
        bot.data = Data()
        file.write(jsonpickle.encode(bot.data))
        print("created new save")

    print("dndbot ready!")


@bot.event
async def on_message(message):
    if message.author == bot.user:  # don't respond to itself
        return
    if message.content.startswith(botprefix):
        await process_command(message)


# ---------------- BOT COMMANDS -----------------

async def process_command(message):
    input_split = message.content[len(botprefix):].split()

    # no commands
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

    # invalid command
    else:
        await message.channel.send("Don't know this command!")


bot.run(TOKEN)
