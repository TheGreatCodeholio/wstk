import datetime
import time

import lib.menu_handler as menu
from lib.text_color import Colors
import lib.command_handler as shell
import os

#########################
# Backup Root Magento No /var
#########################

def backup_magento_basic(config, magento_root_path, backup_path, menu_return):
    action = "Magento Root Backup"
    x = datetime.datetime.now()
    current_date = x.strftime("%d%B%y")
    print(Colors.FG.LightGreen + Colors.Bold + action + " Started." + Colors.Reset)
    if not os.path.exists(backup_path):
        action = "Create Backup Folder"
        shell.run_bash_command(config, magento_root_path, action, "mkdir -p " + backup_path, "Backup Directory Created")
    shell.run_bash_command_popen(config, magento_root_path, action, "tar --exclude=" + magento_root_path + "/var/* -zcf " + backup_path + "/backup_" + current_date + ".tar.gz " + magento_root_path, 1)
    if menu_return == 1:
        menu.magento_menu(config, magento_root_path)

#########################
# Backup Root Magento No Media, No Var
#########################

def backup_magento_no_media(config, magento_root_path, backup_path, menu_return):
    action = "Magento Root Backup"
    x = datetime.datetime.now()
    current_date = x.strftime("%d%B%y")
    print(Colors.FG.LightGreen + Colors.Bold + action + " Started." + Colors.Reset)
    if not os.path.exists(backup_path):
        action = "Create Backup Folder"
        shell.run_bash_command(config, magento_root_path, action, "mkdir -p " + backup_path, "Backup Directory Created")
    shell.run_bash_command_popen(config, magento_root_path, action, "tar --exclude=" + magento_root_path + "/var/* --exclude=" + magento_root_path + "/pub/media/* -zcf " + backup_path + "/backup_" + current_date + ".tar.gz " + magento_root_path, 1)
    if menu_return == 1:
        menu.magento_menu(config, magento_root_path)


#########################
# Static Content Deploy
#########################


def static_content_deploy(config, path):
    action = "Deploy Static Content"
    print(Colors.FG.LightGreen + Colors.Bold + action + " Started." + Colors.Reset)
    shell.run_bash_command(config, path, action,
                           "php -ddisplay_errors=on " + path + "/bin/magento setup:static-content:deploy -f",
                           action + " Completed")


#########################
# Magento Compile
#########################


def magento_compile(config, path):
    action = "Magento Compile"
    print(Colors.FG.LightGreen + Colors.Bold + action + " Started." + Colors.Reset)
    shell.run_bash_command(config, path, action,
                           "php -ddisplay_errors=on " + path + "/bin/magento setup:di:compile",
                           action + " Completed")

#########################
# Magento Setup Upgrade Database
#########################


def magento_setup_upgrade(config, path):
    action = "Magento Setup Upgrade Database"
    print(Colors.FG.LightGreen + Colors.Bold + action + " Started." + Colors.Reset)
    shell.run_bash_command(config, path, action,
                           "php -ddisplay_errors=on " + path + "/bin/magento setup:upgrade",
                           action + " Completed")


#########################
# Index Functions
#########################

def set_index_to_schedule(config, path):
    action = "Set Indexes to Run on Schedule"
    print(Colors.FG.LightGreen + Colors.Bold + action + " Started." + Colors.Reset)
    shell.run_bash_command(config, path, action,
                           "php -ddisplay_errors=on " + path + "/bin/magento indexer:set-mode schedule",
                           action + " Completed")


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
