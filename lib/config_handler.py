#!/usr/bin/env python3
from lib.text_color import Colors
from subprocess import check_output
import json
import os


def get_path():
    path = input(Colors.OKGREEN + "Production public_html path: " + Colors.ENDC)
    if path.endswith('/'):
        print(Colors.FAIL + "Path should not end with a /. Example /srv/public_html" + Colors.ENDC)
        get_path()
        return
    else:
        return path


def load_config(path):
    print(path)
    config = check_output(["php", "-r", "echo json_encode(include '" + path + "/app/etc/env.php');"])
    config = json.loads(config)
    return config


def save_config(config, path):
    if "driver_options" in config["db"]["connection"]["default"]:
        del config["db"]["connection"]["default"]['driver_options']
    with open('/srv/mmtk/var/config.json', 'w') as outfile:
        json.dump(config, outfile)
    os.popen("php -d display_errors=on ./lib/save_config.php " + path)
    print("Configuration Updated")
