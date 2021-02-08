import lib.menu_handler as Menu
from lib.text_color import Colors
import os
import lib.config_handler as Conf
import datetime


def fix_credentials(config, path):
    os.system('/usr/share/stratus/cli database.config > /srv/mmtk/var/cred.log 2>&1')
    db_user = os.popen("cat /srv/mmtk/var/cred.log | grep Username | awk '{print $3}' | cut -c3- | rev | cut -c4- | rev").read().split('\n')[0]
    db_pass = os.popen("cat /srv/mmtk/var/cred.log | grep Username | awk '{print $14}' | cut -c3- | rev | cut -c4- | rev").read().split('\n')[0]
    db_name = os.popen("cat /srv/mmtk/var/cred.log | grep Username | awk '{print $7}' | cut -c3- | rev | cut -c4- | rev").read().split('\n')[0]

    config["db"]["connnection"]["default"]["host"] = "mysql"
    config["db"]["connnection"]["default"]["dbname"] = db_name
    config["db"]["connnection"]["default"]["username"] = db_user
    config["db"]["connnection"]["default"]["password"] = db_pass
    Conf.save_config(config, path)
    Menu.main_menu(config, path)

def mysql_dump(config, path):
    x = datetime.datetime.now()
    current_date = x.strftime("%d%B%y")
    # Check if backups directory exists locally
    if not os.path.exists("/srv/backups/" + current_date):
        os.popen("mkdir /srv/backups" + current_date)
    os.popen("mysqldump --skip-lock-tables --extended-insert=FALSE --verbose -h mysql --quick -u " + config["db"]["connnection"]["default"]["username"] + " -p" + config["db"]["connnection"]["default"]["dbname"] + " " + config["db"]["connnection"]["default"]["password"] + " > /srv/ " + current_date + "/" + config["db"]["connnection"]["default"]["dbname"] + ".sql").read()
    print(Colors.OKGREEN + "MySQL backed up to /srv/backups/" + current_date + "/" + config["db"]["connnection"]["default"]["dbname"] + ".sql" + Colors.ENDC)
    Menu.main_menu(config, path)