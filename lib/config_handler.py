#!/usr/bin/env python3
from lib.text_color import Colors
from subprocess import check_output
import lib.command_handler as shell
import json


def get_path():
    path = input(Colors.FG.LightGreen + Colors.Bold + "Production public_html path: " + Colors.Reset)
    if path.endswith('/'):
        print(Colors.FG.Red + Colors.Bold + "Path should not end with a /. Example /srv/public_html" + Colors.Reset)
        get_path()
        return
    else:
        return path


def load_config(path):
    config = check_output(["php", "-r", "echo json_encode(include '" + path + "/app/etc/env.php');"])
    config = json.loads(config)
    return config


def save_config(config, path):
    action = "Save Config"
    with open('/srv/wstk/var/config.json', 'w+') as outfile:
        json.dump(config, outfile)
    shell.run_bash_command(config, path, action, "php -d display_errors=on ./lib/save_config.php " + path, "")
