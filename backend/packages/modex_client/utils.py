import os
import ast


def save_config_file(data):
    path = os.path.expanduser("~") + "/.modex-client/"
    if os.path.isdir(path) is False:
        os.mkdir(path)
    with open(path + "config", "w") as f:
        f.write(data)


def get_config_file():
    path = os.path.expanduser("~") + "/.modex-client/config"
    if os.path.isfile(path) is True:
        f = open(path, "r")
        return ast.literal_eval(f.read())