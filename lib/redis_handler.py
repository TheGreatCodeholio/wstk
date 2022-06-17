import lib.menu_handler as menu
from lib.text_color import Colors
import lib.command_handler as shell
import lib.config_handler as conf


def check_redis_sessions(config, path):
    if "save" not in config:
        config_sessions(config, path)
    elif "save" in config["queue"]:
        del config["queue"]
        conf.save_config(config, path)
        config_sessions(config, path)
    else:
        config_sessions(config, path)


def check_redis_cache(config, path):
    if "cache" not in config:
        config_cache(config, path)
    elif "cache" in config:
        del config["cache"]
        conf.save_config(config, path)
        config_cache(config, path)
    else:
        config_cache(config, path)


def config_sessions(config, path):
    action = "Configure Redis Sessions"
    shell.run_bash_command(config, path, action,
                           "php -ddisplay_errors=on " + path + "/bin/magento setup:config:set --session-save=redis --session-save-redis-host=redis-session --session-save-redis-log-level=3 --session-save-redis-db=0 --session-save-redis-port=6380 --session-save-redis-disable-locking=1",
                           ".")
    print(Colors.FG.LightGreen + Colors.Bold + action + " Completed!" + Colors.Reset)
    menu.main_menu(path)


def config_cache(config, path):
    action = "Configure Redis FPC and Cache"
    shell.run_bash_command(config, path, action,
                           "php -ddisplay_errors=on " + path + "/bin/magento setup:config:set --cache-backend=redis --cache-backend-redis-server=redis-config-cache --cache-backend-redis-db=0 --cache-backend-redis-port=6381",
                           ".")
    shell.run_bash_command(config, path, action,
                           "php -ddisplay_errors=on " + path + "/bin/magento setup:config:set --page-cache=redis --page-cache-redis-server=redis --page-cache-redis-db=0 --page-cache-redis-port=6379",
                           "..")
    print(Colors.FG.LightGreen + Colors.Bold + action + " Completed!" + Colors.Reset)
    menu.main_menu(path)
