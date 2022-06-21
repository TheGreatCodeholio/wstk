import subprocess
import json
import lib.menu_handler as menu
from lib.text_color import Colors

def run_bash_command_popen(config, path, action, command, success_message):
    child = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    streamdata = child.communicate()[0]
    rc = child.returncode
    if rc == 0:
        if success_message == 1:
            print(Colors.FG.LightGreen + Colors.Bold + action + " complete." + Colors.Reset)
        elif success_message == "":
            return
        else:
            print(Colors.FG.LightGreen + Colors.Bold + success_message + Colors.Reset)
    else:
        print(Colors.FG.Red + Colors.Bold + action + " not completed. Returning to Menu." + Colors.Reset)
        if config is False:
            menu.dev_copy_menu(False, False)
        else:
            menu.main_menu(path)


def run_bash_command(config, path, action, command, success_message):
    running_command = command.split()
    output = subprocess.run(running_command, capture_output=True)
    if output.returncode == 0:
        print(Colors.FG.Green + Colors.Bold + success_message + Colors.Reset)
    else:
        print(Colors.FG.Red + Colors.Bold + "Error executing command. " + command + "\nError Output:\n" + output.stdout.decode("utf-8") + Colors.Reset)
        print(Colors.FG.Red + Colors.Bold + action + " not completed. Returning to Menu." + Colors.Reset)
        menu.main_menu(path)


def run_bash_command_output(command):
    running_command = command.split()
    output = subprocess.run(running_command, capture_output=True)
    return output.stdout.decode('utf-8')


# bin/magento setup:config:set --db-host mysql --db-name --db-user --db-password
def load_json_from_command(command):
    running_command = command.split()
    output = subprocess.run(running_command, capture_output=True)
    if output.returncode == 0:
        result = json.loads(output.stdout.decode('utf-8'))
        return result
    else:
        return False
