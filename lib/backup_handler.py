import datetime

import lib.menu_handler as menu
from lib.text_color import Colors
import lib.command_handler as shell
import lib.mysql_handler as mysql
import lib.magento_handler as magento


def backup_to_s3_bucket(config, path, menu_return):
    x = datetime.datetime.now()
    current_date = x.strftime("%d%B%y")
    action = "S3 Bucket Upload"
    print(Colors.FG.LightGreen + "Starting " + action + Colors.Reset)
    s3_bucket = input(Colors.FG.Yellow + "S3 Bucket Name: " + Colors.Reset)
    mysql.mysql_dump_auto(config, path, path + "/database", 0)
    magento.backup_magento_basic(config, path, "/srv", 0)
    shell.run_bash_command_popen(config, path, action, "aws s3 cp /srv/backup_" + current_date + ".tar.gz s3://" + s3_bucket, 1)
    action = "Backup Cleanup"
    print(Colors.FG.LightGreen + "Starting " + action + Colors.Reset)
    action = "Remove Backup Archive"
    shell.run_bash_command_popen(config, path, action, "rm -f /srv/backup_" + current_date + ".tar.gz", 1)
    action = "Remove Backup Database"
    shell.run_bash_command_popen(config, path, action, "rm -rf " + path + "/database", 1)
    menu.magento_backup_menu(config, path)

def backup_local_auto(config, path, media, menu_return):
    x = datetime.datetime.now()
    current_date = x.strftime("%d%B%y")
    action = "Magento Local Backup"
    print(Colors.FG.LightGreen + "Starting " + action + Colors.Reset)
    mysql.mysql_dump_auto(config, path, path + "/database", 0)
    if media == 1:
        magento.backup_magento_basic(config, path, "/srv/backups/" + current_date, 0)
    else:
        magento.backup_magento_no_media(config, path, "/srv/backups/" + current_date, 0)

    action = "Backup Cleanup"
    print(Colors.FG.LightGreen + "Starting " + action + Colors.Reset)
    shell.run_bash_command_popen(config, path, action, "rm -rf " + path + "/database", 1)

    print(Colors.FG.LightGreen + "Magento Local Backup Complete: " + "/srv/backups/" + current_date + "/backup_" + current_date + ".tar.gz" + Colors.Reset)
    menu.magento_backup_menu(config, path)

def backup_local_custom(config, path, media, menu_return):
    x = datetime.datetime.now()
    current_date = x.strftime("%d%B%y")
    action = "Magento Local Backup"
    print(Colors.FG.LightGreen + "Starting " + action + Colors.Reset)
    mysql.mysql_dump_auto(config, path, path + "/database", 0)
    backup_path = input(Colors.FG.Yellow + "Backup Path: Default - /srv/backups: " + Colors.Reset)
    if backup_path == "":
        backup_path = "/srv/backups"
    elif backup_path.endswith("/"):
        path_length = len(backup_path)
        backup_path = backup_path[:path_length - 1]
    if media == 1:
        magento.backup_magento_basic(config, path, backup_path + "/" + current_date, 0)
    else:
        magento.backup_magento_no_media(config, path, backup_path + "/" + current_date, 0)

    action = "Backup Cleanup"
    print(Colors.FG.LightGreen + "Starting " + action + Colors.Reset)
    shell.run_bash_command_popen(config, path, action, "rm -rf " + path + "/database", 1)

    print(Colors.FG.LightGreen + "Magento Local Backup Complete: " + backup_path + "/" + current_date + "/backup_" + current_date + ".tar.gz" + Colors.Reset)
    menu.magento_backup_menu(config, path)