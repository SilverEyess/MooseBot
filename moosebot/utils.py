import json
import os
import shutil

import requests


def save(list, path):
    with open(path, 'w') as write_file:
        json.dump(list, write_file, indent=4)


def load(path):
    firstline = dict()
    if os.path.exists(path):
        with open(path, 'r') as read_file:
            data = json.load(read_file)
        return data
    else:
        s = json.dumps(firstline)
        with open(path, 'w+') as new_file:
            new_file.write(s)
            try:
                data = json.load(new_file)

            except json.JSONDecodeError:
                data = dict()
            return data


def get_image(url):
    response = requests.get(url, stream=True)
    return response.raw


def save_image(folder, name, data, filetype=None):
    filetype = filetype or ".png"
    if name == "temp_image":
        file_name = os.path.join(folder, name + filetype)
        with open(file_name, 'wb') as fout:
            shutil.copyfileobj(data, fout)
    else:
        file_name = os.path.join(folder, name + filetype)
        if os.path.exists(file_name):
            name = name + "_1"
            file_name = os.path.join(folder, name + filetype)
            with open(file_name, 'wb') as fout:
                shutil.copyfileobj(data, fout)
        else:
            with open(file_name, 'wb') as fout:
                shutil.copyfileobj(data, fout)


async def check_con(bot, ctx):
    vcs = [i.guild for i in bot.client.voice_clients]
    if ctx.guild in vcs:
        return True
    else:
        return False
