import shutil

import lib.menu_handler as menu
import lib.config_handler as conf
import os


def main():
    path = conf.get_path()
    version = str(os.popen("cd " + path + " && n98-magerun2 sys:info | awk 'NR==10 { print $4;exit }'").readlines()[0]).replace("\n", "")
    major = version.split("-")[0].split(".")[0]
    minor = version.split("-")[0].split(".")[1]

    if int(major) != 2:
        print("Script Requires Magento 2.3 or 2.4 Your version: " + version)
        exit()
    elif int(minor) < 3 or int(minor) > 4:
        print("Script Requires Magento 2.3 or 2.4. Your version: " + version)
        exit()

    if os.path.exists(path + "/app/etc/env.php"):
        source = path + "/app/etc/env.php"
        dest = "/srv/wstk/var/"
        shutil.copytree(source, dest)

    if os.path.exists(path + "/composer.json"):
        source = path + "/app/etc/composer.json"
        dest = "/srv/wstk/var/"
        shutil.copytree(source, dest)

    menu.main_menu(path)


main()
