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

    config["db"]["connection"]["default"]["host"] = "mysql"
    config["db"]["connection"]["default"]["dbname"] = db_name
    config["db"]["connection"]["default"]["username"] = db_user
    config["db"]["connection"]["default"]["password"] = db_pass
    Conf.save_config(config, path)
    Menu.main_menu(config, path)

def mysql_dump(config, path):
    x = datetime.datetime.now()
    current_date = x.strftime("%d%B%y")
    # Check if backups directory exists locally
    if not os.path.exists("/srv/backups/"):
        os.popen("mkdir /srv/backups/")
    if not os.path.exists("/srv/backups/" + current_date + "/"):
        os.popen("mkdir /srv/backups/" + current_date + "/")
    os.popen("mysqldump --skip-lock-tables --extended-insert=FALSE --verbose -h mysql --quick -u " + config["db"]["connection"]["default"]["username"] + " -p" + config["db"]["connection"]["default"]["password"] + " " + config["db"]["connection"]["default"]["dbname"] + " > /srv/backups/" + current_date + "/" + config["db"]["connection"]["default"]["dbname"] + ".sql").read()
    print(Colors.OKGREEN + "MySQL backed up to /srv/backups/" + current_date + "/" + config["db"]["connection"]["default"]["dbname"] + ".sql" + Colors.ENDC)
    Menu.main_menu(config, path)