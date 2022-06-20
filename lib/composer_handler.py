from lib.text_color import Colors
import lib.command_handler as shell
import json


def load_composer_json(config, path):
    with open(path + "/composer.json", "r") as cjson:
        composer_config = json.load(cjson)
    cjson.close()
    if composer_config:
        return composer_config
    else:
        return False


def save_composer_json(config, path, composer_data):
    with open(path + "/composer.json", "w+") as cjson:
        json.dump(composer_data, cjson, indent=4)
    cjson.close()


def composer_check_cweagans(config, path):
    cweagans = False
    with open(path + "/composer.json", "r") as cjson:
        composer_config = json.load(cjson)
    cjson.close()
    if composer_config:
        if "require" in composer_config:
            if "cweagans/composer-patches" in composer_config["require"]:
                cweagans = True

    return cweagans


def install_cweagans(config, path):
    result = composer_check_cweagans(config, path)
    action = "Install cweagans"
    if result is False:
        shell.run_bash_command_popen(config, path, action, "cd " + path + "&& composer require cweagans/composer-patches", 1)
    else:
        print(Colors.FG.LightGreen + Colors.Bold + action + " already completed." + Colors.Reset)


def composer_install(config, path):
    action = "Composer Install"
    shell.run_bash_command_popen(config, path, action, "cd " + path + "&& composer -v install", 1)


def composer_lock(config, path):
    action = "Composer Update Lock"
    shell.run_bash_command_popen(config, path, action, "cd " + path + "&& composer update --lock", 1)
