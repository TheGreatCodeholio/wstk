import lib.menu_handler as Menu
from lib.text_color import Colors
import lib.config_handler as Conf
import os


def install_mmcron(config, path):
    os.popen("cd " + path + " && composer require magemojo/m2-ce-cron").read()
    os.popen("php " + path + "/bin/magento module:enable MageMojo_Cron").read()
    os.popen("php " + path + "/bin/magento setup:upgrade").read()
    os.popen("php " + path + "/bin/magento setup:di:compile").read()
    os.popen("php " + path + "/bin/magento setup:static-content:deploy -f").read()
    print(Colors.OKGREEN + "MageMojo Cron Installed" + Colors.ENDC)
    Menu.main_menu(config, path)

def reset_crons(config, path):
    os.popen("mysql -h mysql -u " + config["db"]["connection"]["default"]["username"] + " -p\"" + config["db"]["connection"]["default"]["password"] + "\" " + config["db"]["connection"]["default"]["dbname"] + " -e 'delete from " + config["db"]["table_prefix"] + "cron_schedule'").read()
    os.popen("pkill -f cron & pkill -f cron & rm -rf " + path + "/var/cron/* ").read()
    print(Colors.OKGREEN + "Reset Crons" + Colors.ENDC)
    Menu.main_menu(config, path)