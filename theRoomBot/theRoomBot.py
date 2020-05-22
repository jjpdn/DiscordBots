import random
import os.path
import jsonpickle
import asyncio
from threading import Thread
from discord.ext import commands


class Data(object):
    def __init__(self):
        self.main_channel = None
        self.inventory = []
        self.state = 0
        self.map_msg_id = -1
        self.progress_msg_id = {}
        self.cooldown = {}
        self.light_lvl = 0

async def set_timer(data, name, duration, sleep_segments = 5):
    # add timer result to cooldowns
    if not name in data.cooldown.keys():
        data.cooldown[name] = -1
        data.progress_msg_id[name] = -1
    if data.cooldown[name] == -1:
        progress_bar = list('`' + '-' * sleep_segments + '`') # 10 * '-'
        if data.progress_msg_id[name] == -1:
            message = await data.main_channel.send(''.join(progress_bar))
            data.progress_msg_id[name] = message.id
        else:
            message = await data.main_channel.fetch_message(data.progress_msg_id[name])
            await message.edit(content = progress_bar)

        # count down in segments with length of segment_duration
        data.cooldown[name] = 0
        segment_duration = duration / sleep_segments
        while sleep_segments > 0:
            await asyncio.sleep(segment_duration)
            sleep_segments -= 1
            progress_bar[len(progress_bar) - sleep_segments - 2] = 'M'
            await message.edit(content = ''.join(progress_bar))
        data.cooldown[name] = 1
    else:
        data.main_channel.send("ERROR timer not reset")

async def darkness(data):

    light_messages = ["It is dark.", "There is but a bare flicker.", "The light dims.", "The fire burns strong."]

    while True:
        if data.light_lvl > 0:
            data.light_lvl -= 1
            await data.main_channel.send(light_messages[data.light_lvl])
        await asyncio.sleep(4)


# --------------- BOT SETUP ------------------

token_file = open("../data/roomtoken", "r")
TOKEN = token_file.read()
data_path = "../data/roomdata.json"
botprefix = '!'

bot = commands.Bot(botprefix)

@bot.event
async def on_connect():
    # variables
    bot.number_pool = list(range(5))
    random.shuffle(bot.number_pool)
    # read saves
    if (os.path.isfile(data_path)):
        file = open(data_path)
        bot.data = jsonpickle.decode(file.read())
        print("loaded old save")
    else:
        bot.data = Data()
        file = open(data_path,'w+')
        file.write(jsonpickle.encode(bot.data))
        print("created new save")

    asyncio.create_task(darkness(bot.data))

    print("roombot ready!")


@bot.event
async def on_message(message):
    if message.author == bot.user:  # don't respond to itself
        return
    if message.content.startswith(botprefix):
        await process_command(message)


# ---------------- BOT COMMANDS -----------------

async def process_command(message):
    input_split = message.content[len(botprefix):].split()

    # /// General Commands ///

    # no commands
    if len(input_split) == 0:
        await message.channel.send("Don't know this command!")
        return

    cmd = input_split[0]
    modifiers = input_split[1:]

    if cmd.lower() == 'hello':
        await message.channel.send("Hello!")
        return

    elif cmd == 'getnum':
        if len(bot.number_pool) != 0:
            num = bot.number_pool.pop()
            await message.author.send("Your secret number is: " + str(num))
        else:
            await message.author.send("Out of numbers!")
        return

    elif cmd == 'rnum':
        rnum = len(bot.number_pool)
        await message.channel.send("Remaining number of numbers: " + str(rnum))
        return

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

        return

    elif cmd == 'setmain':
        bot.data.main_channel = message.channel
        await message.channel.send("Set this channel as main channel!")
        return
    else:

        # /// Beginning ///

        if bot.data.state == 0:

            if cmd == "trytimer":
                if bot.data.main_channel == None:
                    await message.channel.send("ERROR: main channel not set. Please use !setmain to set current channel" + \
                            " as main channel.")
                else:
                    #timer_thread = Thread(target=await set_timer(bot.data, "temp", 5))
                    task = asyncio.create_task(set_timer(bot.data, "temp", 10))
                    #timer_thread.start()
                    # timer_thread = Thread(target=await set_timer(bot.data, "temp2", 10))
                    # timer_thread.start()
                    # task = asyncio.create_task(set_timer(bot.data, "temp2", 10))
                return

        await message.channel.send("Don't know this command!")


bot.run(TOKEN)
