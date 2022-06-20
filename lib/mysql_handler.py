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


def update_mysql_credentials_manual(config, path, menu_return):
    action = "Update MySQL Credentials"
    db_creds = {}
    db_creds["Name"] = input(Colors.FG.Yellow + "MySQL Database: " + Colors.Reset)
    db_creds["Username"] = input(Colors.FG.Yellow + "MySQL Username: " + Colors.Reset)
    db_creds["Password"] = input(Colors.FG.Yellow + "MySQL Password: " + Colors.Reset)

    if db_creds is not False:
        shell.run_bash_command_popen(config, path, action,
                               "php -ddisplay_errors=on " + path + "/bin/magento setup:config:set --db-host mysql --db-name " + db_creds[
                                   "Name"] + " --db-user " + db_creds["Username"] + " --db-password " + db_creds[
                                   "Password"], 1)
        print(Colors.FG.LightGreen + Colors.Bold + action + " Completed!" + Colors.Reset)
    else:
        print(Colors.FG.Red + Colors.Bold + "Error getting database credentials." + Colors.Reset)
        print(Colors.FG.Red + Colors.Bold + action + " not completed. Returning to Menu." + Colors.Reset)
    if menu_return == 1:
        menu.mysql_menu(config, path)


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
    shell.run_bash_command_popen(config, magento_root_path, action, "mysqldump --no-tablespaces --skip-lock-tables --opt --single-transaction --max_allowed_packet=512M -h mysql -u " + config["db"]["connection"]["default"]["username"] + " -p" + config["db"]["connection"]["default"]["password"] + " " + config["db"]["connection"]["default"]["dbname"] + " > " + backup_path + "/" + current_date + "_" + config["db"]["connection"]["default"]["dbname"] + ".sql", 1)
    print(Colors.FG.LightGreen + Colors.Bold + "MySQL Database Backed up to: " + backup_path + "/" + current_date + "_" + config["db"]["connection"]["default"][
        "dbname"] + ".sql" + Colors.Reset)

    if menu_return == 1:
        menu.mysql_menu(config, magento_root_path)

def mysql_dump_manual(config, magento_root_path, menu_return):
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
                           db_name + ".sql", 1)
    print(Colors.FG.LightGreen + Colors.Bold + "MySQL Database Backed up to: " + backup_path + "/" + current_date + "_" + db_name + ".sql" + Colors.Reset)
    if menu_return == 1:
        menu.mysql_menu(config, magento_root_path)

def backup_remote_database(settings_dict):
    # Get Remote Database Credentials via SSH
    print(Colors.FG.LightGreen + Colors.Bold + "Getting Production Database Credentials." + Colors.Reset)
    dump_creds = os.popen("ssh -i " + settings_dict["prod_ssh_privkey_path"] + " " + settings_dict["prod_ssh_user"] + "@" + settings_dict["prod_ssh_host"] + " -p" + settings_dict["prod_ssh_port"] + " '/usr/share/stratus/cli database.config > cred.log 2>&1; cat cred.log'").read()
    os.popen("ssh -i " + settings_dict["prod_ssh_privkey_path"] + " " + settings_dict["prod_ssh_user"] + "@" + settings_dict["prod_ssh_host"] + " -p" + settings_dict["prod_ssh_port"] + " 'rm cred.log'")
    cred_file = open("remote_creds.log", "w")
    cred_file.write(dump_creds)
    cred_file.close()
    # Read Credentials to our settings Dictionary
    settings_dict["prod_mysql_user"] = os.popen("cat remote_creds.log | grep Username | awk '{print $3}' | cut -c3- | rev | cut -c4- | rev").read().split('\n')[0]
    settings_dict["prod_mysql_database"] = os.popen("cat remote_creds.log | grep Username | awk '{print $7}' | cut -c3- | rev | cut -c4- | rev").read().split('\n')[0]
    settings_dict["prod_mysql_password"] = os.popen("cat remote_creds.log | grep Username | awk '{print $14}' | cut -c3- | rev | cut -c4- | rev").read().split('\n')[0]
    os.popen("rm remote_creds.log")
    # MySQL Dump Database
    print(Colors.FG.LightGreen + Colors.Bold + "Dumping Production Database." + Colors.Reset)
    os.popen("ssh -i " + settings_dict["prod_ssh_privkey_path"] + " " + settings_dict["prod_ssh_user"] + "@" + settings_dict["prod_ssh_host"] + " -p" + settings_dict["prod_ssh_port"] + " 'mysqldump --no-tablespaces --skip-lock-tables --opt --single-transaction --max_allowed_packet=512M -h mysql --quick -u " + settings_dict["prod_mysql_user"] + " -p" + settings_dict["prod_mysql_password"] + " " + settings_dict["prod_mysql_database"] + " > /srv/db_" + settings_dict["current_date"] + ".sql'").read()
    # Check if backups directory exists locally
    if not os.path.exists("/srv/backups"):
        os.popen("mkdir /srv/backups")
    # RSYNC Database Dump to Local backups folder.
    print(Colors.FG.LightGreen + Colors.Bold + "RSYNC Production Database to Dev." + Colors.Reset)
    os.popen("rsync -Pav -e 'ssh -p " + settings_dict["prod_ssh_port"] + " -i " + settings_dict["prod_ssh_privkey_path"] + "' " + settings_dict["prod_ssh_user"] + "@" + settings_dict["prod_ssh_host"] + ":/srv/db_" + settings_dict["current_date"] + ".sql /srv/backups/").read()
    # Finished with database backup.

def import_remote_database(settings_dict):
    # Fix SUPER Privs
    print(Colors.FG.LightGreen + Colors.Bold + "Fixing Super Privileges." + Colors.Reset)
    action = "Fix Super Privileges"
    shell.run_bash_command_popen(False, False, action, "sed -i 's/DEFINER=[^*]*\*/\*/g' /srv/backups/db_" + settings_dict["current_date"] + ".sql", 1)
    # Drop Old Database
    os.popen("mysql -h mysql -u " + settings_dict["dev_mysql_user"] + " -p'" + settings_dict["dev_mysql_password"] + "' -e 'drop database " + settings_dict["dev_mysql_database"] + "'").read()
    # Create Blank Database
    os.popen("mysql -h mysql -u " + settings_dict["dev_mysql_user"] + " -p'" + settings_dict["dev_mysql_password"] + "' -e 'create database " + settings_dict["dev_mysql_database"] + "'").read()
    # Import Fixed Dump
    print(Colors.FG.LightGreen + Colors.Bold + "Importing Production Database to Dev." + Colors.Reset)
    os.popen("mysql -h mysql -u " + settings_dict["dev_mysql_user"] + " -p'" + settings_dict["dev_mysql_password"] + "' " + settings_dict["dev_mysql_database"] + " < /srv/backups/db_" + settings_dict["current_date"] + ".sql").read()
    # Remove fixed database, keeping synced one for backup.
    os.popen("rm /srv/backups/db_" + settings_dict["current_date"] + ".sql")
    # Finished Import