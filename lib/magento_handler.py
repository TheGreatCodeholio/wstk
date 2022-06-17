import time

import lib.menu_handler as menu
from lib.text_color import Colors
import lib.command_handler as shell
import os


#########################
# Index Functions
#########################

def reindex_one_index(config, path, index):
    action = "Reindex: " + index.replace("_", " ").capitalize()
    print(Colors.FG.LightGreen + Colors.Bold + action + " Started." + Colors.Reset)
    shell.run_bash_command(config, path, action,
                           "php -ddisplay_errors=on " + path + "/bin/magento indexer:reindex " + index,
                           action + " Completed")


def reindex_all_index(config, path):
    action = "Reindex all Indexes"
    print(Colors.FG.LightGreen + Colors.Bold + action + " Started." + Colors.Reset)
    shell.run_bash_command(config, path, action,
                           "php -ddisplay_errors=on " + path + "/bin/magento indexer:reindex",
                           action + " Completed")


def reset_one_index(config, path, index):
    action = "Reset Index: " + index.replace("_", " ").capitalize()
    print(Colors.FG.LightGreen + Colors.Bold + action + " Started." + Colors.Reset)
    shell.run_bash_command(config, path, action,
                           "php -ddisplay_errors=on " + path + "/bin/magento indexer:reset " + index,
                           action + " Completed")


def reset_all_index(config, path):
    action = "Reset all Indexes"
    print(Colors.FG.LightGreen + Colors.Bold + action + " Started." + Colors.Reset)
    shell.run_bash_command(config, path, action,
                           "php -ddisplay_errors=on " + path + "/bin/magento indexer:reset",
                           action + " Completed")
