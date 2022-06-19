import json

import lib.menu_handler as menu
from lib.text_color import Colors
import os
import lib.command_handler as shell
import lib.config_handler as conf
import datetime


def update_mysql_credentials_from_system(config, path, menu_return):
    action = "Update MySQL Credentials"
    db_creds = get_mysql_credentials()
    if db_creds is not False:
        config["db"]["connection"]["default"]["host"] = "mysql"
        config["db"]["connection"]["default"]["dbname"] = db_creds["Name"]
        config["db"]["connection"]["default"]["username"] = db_creds["Username"]
        config["db"]["connection"]["default"]["password"] = db_creds["Password"]
        conf.save_config(config, path)
        print(Colors.FG.LightGreen + Colors.Bold + action + " Completed!" + Colors.Reset)
    else:
        print(Colors.FG.Red + Colors.Bold + "Error getting database credentials from Stratus CLI" + Colors.Reset)
        print(Colors.FG.Red + Colors.Bold + action + " not completed. Returning to Menu." + Colors.Reset)
    if menu_return == 1:
        menu.main_menu(path)


def update_mysql_credentials_manual(config, path):
    action = "Update MySQL Credentials"
    db_creds = {}
    db_creds["Name"] = input(Colors.FG.Yellow + "MySQL Database: " + Colors.Reset)
    db_creds["Username"] = input(Colors.FG.Yellow + "MySQL Username: " + Colors.Reset)
    db_creds["Password"] = input(Colors.FG.Yellow + "MySQL Password: " + Colors.Reset)

    if db_creds is not False:
        shell.run_bash_command_popen(config, path, action,
                               "php -ddisplay_errors=on " + path + "/bin/magento setup:config:set --db-host mysql --db-name " + db_creds[
                                   "Name"] + " --db-user " + db_creds["Username"] + " --db-password " + db_creds[
                                   "Password"])
        print(Colors.FG.LightGreen + Colors.Bold + action + " Completed!" + Colors.Reset)
    else:
        print(Colors.FG.Red + Colors.Bold + "Error getting database credentials." + Colors.Reset)
        print(Colors.FG.Red + Colors.Bold + action + " not completed. Returning to Menu." + Colors.Reset)
    menu.main_menu(path)


def get_mysql_credentials():
    os.system('/usr/share/stratus/cli database.config > /srv/wstk/var/cred.log 2>&1')
    result = shell.load_json_from_command("head -n1 /srv/wstk/var/cred.log")
    if result is not False:
        db_creds = json.loads(result["args"][0].replace("Result:", ""))
        return db_creds
    else:
        return False


def mysql_dump_auto(config, magento_root_path, backup_path, menu_return):
    x = datetime.datetime.now()
    current_date = x.strftime("%d%B%y")
    # Check if backups directory exists locally
    if not os.path.exists(backup_path):
        action = "Create Backup Folder"
        shell.run_bash_command(config, magento_root_path, action, "mkdir -p " + backup_path, "Backup Directory Created")

    if os.path.exists(backup_path + "/" + current_date + "_" + config["db"]["connection"]["default"]["dbname"] + ".sql"):
        os.remove(backup_path + "/" + current_date + "_" + config["db"]["connection"]["default"]["dbname"] + ".sql")

    action = "Database Backup"
    shell.run_bash_command_popen(config, magento_root_path, action, "mysqldump --no-tablespaces --skip-lock-tables --opt --single-transaction --max_allowed_packet=512M -h mysql -u " + config["db"]["connection"]["default"]["username"] + " -p" + config["db"]["connection"]["default"]["password"] + " " + config["db"]["connection"]["default"]["dbname"] + " > " + backup_path + "/" + current_date + "_" + config["db"]["connection"]["default"]["dbname"] + ".sql")
    print(Colors.FG.LightGreen + Colors.Bold + "MySQL Database Backed up to: " + backup_path + "/" + current_date + "_" + config["db"]["connection"]["default"][
        "dbname"] + ".sql" + Colors.Reset)

    if menu_return == 1:
        menu.mysql_menu(config, magento_root_path)

def mysql_dump_manual(config, magento_root_path):
    x = datetime.datetime.now()
    current_date = x.strftime("%d%B%y")
    backup_path = input(Colors.FG.Yellow + "Path to dump database to? Default: /srv/backups: " + Colors.Reset)
    if backup_path == "":
        backup_path = "/srv/backups"
    elif backup_path.endswith("/"):
        path_length = len(backup_path)
        backup_path = backup_path[:path_length - 1]

    db_name = input(Colors.FG.Yellow + "MySQL Database: " + Colors.Reset)
    db_username = input(Colors.FG.Yellow + "MySQL Username: " + Colors.Reset)
    db_password = input(Colors.FG.Yellow + "MySQL Password: " + Colors.Reset)

    # Check if backups directory exists locally
    if not os.path.exists(backup_path):
        action = "Create Backup Folder"
        shell.run_bash_command(config, magento_root_path, action, "mkdir -p " + backup_path, "Backup Directory Created")

    if os.path.exists(backup_path + "/" + current_date + "_" + db_name + ".sql"):
        os.remove(backup_path + "/" + current_date + "_" + db_name + ".sql")

    action = "Database Backup"
    shell.run_bash_command_popen(config, magento_root_path, action,
                           "mysqldump --no-tablespaces --skip-lock-tables --opt --single-transaction --max_allowed_packet=512M -h mysql -u " +
                           db_username + " -p" +
                           db_password + " " +
                           db_name + " > " + backup_path + "/" + current_date + "_" +
                           db_name + ".sql")
    print(Colors.FG.LightGreen + Colors.Bold + "MySQL Database Backedup to: " + backup_path + "/" + current_date + "_" + db_name + ".sql" + Colors.Reset)
    menu.main_menu(magento_root_path)
