import lib.menu_handler as Menu
from lib.text_color import Colors
import os


def clear_magento(config, path):
    os.popen("php " + path + "/bin/magento cache:flush").read()
    os.popen("php " + path + "/bin/magento cache:clear").read()
    print(Colors.OKGREEN + "Cleared Magento Cache" + Colors.ENDC)
    Menu.main_menu(config, path)


def clear_redis(config, path):
    os.popen("redis-cli -h redis flushall").read()
    print(Colors.OKGREEN + "Cleared Redis Cache" + Colors.ENDC)
    Menu.main_menu(config, path)


def clear_cloudfront(config, path):
    os.popen("/usr/share/stratus/cli cache.all.clear").read()
    print(Colors.OKGREEN + "Cleared CloudFront Cache" + Colors.ENDC)
    Menu.main_menu(config, path)


def reinit_as(config, path):
    os.popen("/usr/share/stratus/cli autoscaling.reinit").read()
    print(Colors.OKGREEN + "Reinitalized Autoscaling" + Colors.ENDC)
    Menu.main_menu(config, path)


def reinit_as_zdd(config, path):
    os.popen("/usr/share/stratus/cli zerodowntime.init && /usr/share/stratus/cli zerodowntime.switch").read()
    print(Colors.OKGREEN + "Reinitalized Autoscaling" + Colors.ENDC)
    Menu.main_menu(config, path)


def clear_all(config, path):
    os.popen("php " + path + "/bin/magento cache:flush").read()
    os.popen("php " + path + "/bin/magento cache:clear").read()
    os.popen("redis-cli -h redis flushall").read()
    os.popen("/usr/share/stratus/cli cache.all.clear").read()
    print(Colors.OKGREEN + "Cleared All Caches" + Colors.ENDC)
    Menu.main_menu(config, path)
