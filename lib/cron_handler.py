import time

import lib.menu_handler as menu
from lib.text_color import Colors
import lib.command_handler as shell


def install_mmcron(config, path, menu_return):
    action = "Install MageMojo Cron Module"

    print(Colors.FG.LightGreen + "Adding magemojo/m2-me-cron to Composer")
    shell.run_bash_command(config, path, action, "cd " + path + " && composer require magemojo/m2-ce-cron", "Installed MageMojo Cron With Composer")
    print(Colors.FG.LightGreen + "Enabling Module in Magento.")
    shell.run_bash_command(config, path, action, "php -ddisplay_errors=on " + path + "/bin/magento module:enable MageMojo_Cron", "Enabled MageMojo_Cron in Magento 2")
    print(Colors.FG.LightGreen + "Running Magento setup:upgrade")
    shell.run_bash_command(config, path, action, "php -ddisplay_errors=on " + path + "/bin/magento setup:upgrade", "Ran Magento 2 setup:upgrade.")
    print(Colors.FG.LightGreen + "Starting Magento Compile")
    shell.run_bash_command(config, path, action, "php -ddisplay_errors=on " + path + "/bin/magento setup:di:compile", "Magento 2 Compile Complete")
    print(Colors.FG.LightGreen + "Starting Static Content Deploy")
    shell.run_bash_command(config, path, action, "php -ddisplay_errors=on " + path + "/bin/magento setup:static-content:deploy -f", "Magento 2 Static Content Deploy Complete")
    print(Colors.FG.LightGreen + Colors.Bold + action + " Completed." + Colors.Reset)
    time.sleep(1.5)
    if menu_return == 1:
        menu.cron_menu(config, path)


def reset_crons(config, path, menu_return):
    action = "Reset Crons"
    shell.run_bash_command(config, path, "Stop Crons", "/usr/share/stratus/cli crons.stop", "Stopped Cron Jobs")
    shell.run_bash_command_popen(config, path, "Delete Cron Schedule from Database", "mysql -h mysql -u " + config["db"]["connection"]["default"]["username"] + " -p\"" +
             config["db"]["connection"]["default"]["password"] + "\" " + config["db"]["connection"]["default"][
                 "dbname"] + " -e 'delete from " + config["db"]["table_prefix"] + "cron_schedule'", 1)
    shell.run_bash_command(config, path, action, "rm -rf " + path + "/var/cron/*", "Cleared " + path + "/var/cron/")
    shell.run_bash_command(config, path, action, "/usr/share/stratus/cli crons.start", "Started Cron Jobs")
    print(Colors.FG.LightGreen + Colors.Bold + action + " Completed." + Colors.Reset)
    time.sleep(1.5)
    if menu_return == 1:
        menu.cron_menu(config, path)