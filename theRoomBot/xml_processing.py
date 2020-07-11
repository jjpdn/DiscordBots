

# process a line of text without the
def process_text_segment(message, parameters):
    return message


# send a message in the channel after processing it
async def send_loaded_message(title, messages_dict, channel, parameters=None):

    # split into multiple lines
    text = process_text_segment(messages_dict[title]["body"], parameters)
    split_text = text.split("\n")

    for line in split_text:
        await channel.send(process_text_segment(line, parameters))

class StoryStep:
    story_step_id = -1

    '''
    xml format for a "story step"
        
    '''
    def __init__(self, step_dict):
        return
