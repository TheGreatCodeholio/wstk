import lib.menu_handler as menu
import lib.config_handler as conf
import os


def main():
    version = str(os.popen("n98-magerun2 sys:info | awk 'NR==10 { print $4;exit }'").readlines()[0]).replace("\n", "")
    major = version.split("-")[0].split(".")[0]
    minor = version.split("-")[0].split(".")[1]

    if int(major) != 2:
        print("Script Requires Magento 2.3 or 2.4 Your version: " + version)
        exit()
    elif int(minor) < 3 or int(minor) > 4:
        print("Script Requires Magento 2.3 or 2.4. Your version: " + version)
        exit()

    path = str(os.popen("n98-magerun2 sys:info | awk 'NR==12 { print $4;exit }'").readlines()[0]).replace("\n", "")
    menu.main_menu(path)


main()
