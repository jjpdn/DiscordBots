import asyncio

async def set_timer(data, name, duration, channel, sleep_segments = 5):
    # add timer result to cooldowns
    if not name in data.cooldown.keys():
        data.cooldown[name] = -1
        data.progress_msg_id[name] = -1
    if data.cooldown[name] == -1:
        progress_bar = list('`' + '-' * sleep_segments + '`') # 10 * '-'
        if data.progress_msg_id[name] == -1:
            message = await channel.send(''.join(progress_bar))
            data.progress_msg_id[name] = message.id
        else:
            message = await channel.fetch_message(data.progress_msg_id[name])
            await message.edit(content = ''.join(progress_bar))

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
        channel.send("ERROR timer not reset")

async def darkness(data, channel):

    light_messages = ["It is dark. Too dark.", "Shadows encroach.", "It flickers.", "Its light dims.", "The fire is warm."]

    while True:
        if data.light_lvl > 0:
            data.light_lvl -= 1
            await channel.send(light_messages[data.light_lvl])
        await asyncio.sleep(10)

async def stoke_fire(message, data, channel):
    await channel.send(message.author.display_name + " stoke the fire.")
    data.light_lvl = 5
    await message.channel.send("The fire burns bright.")