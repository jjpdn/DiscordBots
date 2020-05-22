import os.path
import jsonpickle

data_path = "../data/roomdata.json"


class Data(object):
    def __init__(self):
        self.main_channel_id = -1
        self.inventory = []
        self.state = 0
        self.map_msg_id = -1
        self.progress_msg_id = {}
        self.cooldown = {}
        self.light_lvl = 0


def read_saves():
    if os.path.isfile(data_path):
        file = open(data_path)
        data = jsonpickle.decode(file.read())
        print("loaded old save")
    else:
        data = Data()
        file = open(data_path, 'w+')
        file.write(jsonpickle.encode(data))
        print("created new save")

    return data


def save(data):
    file = open(data_path, 'w+')
    file.write(jsonpickle.encode(data))


def reset():
    data = Data()
    file = open(data_path, 'w+')
    file.write(jsonpickle.encode(data))
    print("created new save")
    return data