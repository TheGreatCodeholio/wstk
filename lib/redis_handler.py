import lib.menu_handler as menu
from lib.text_color import Colors
import lib.command_handler as shell
import lib.config_handler as conf


def check_redis_sessions(config, path, menu_return):
    if "save" not in config:
        config_sessions(config, path, menu_return)
    elif "save" in config:
        del config["save"]
        conf.save_config(config, path)
        config_sessions(config, path, menu_return)
    else:
        config_sessions(config, path, menu_return)


def check_redis_cache(config, path, menu_return):
    if "cache" not in config:
        config_cache(config, path, menu_return)
    elif "cache" in config:
        del config["cache"]
        conf.save_config(config, path)
        config_cache(config, path, menu_return)
    else:
        config_cache(config, path, menu_return)


def config_sessions(config, path, menu_return):
    action = "Configure Redis Sessions"
    print(Colors.FG.LightGreen + Colors.Bold + action + " Started" + Colors.Reset)
    shell.run_bash_command_popen(config, path, action,
                           "php -ddisplay_errors=on " + path + "/bin/magento setup:config:set --session-save=redis --session-save-redis-host=redis-session --session-save-redis-log-level=3 --session-save-redis-db=0 --session-save-redis-port=6380 --session-save-redis-disable-locking=1", 1)
    print(Colors.FG.LightGreen + Colors.Bold + action + " Completed!" + Colors.Reset)
    if menu_return == 1:
        menu.redis_menu(config, path)


def config_cache(config, path, menu_return):
    action = "Configure Redis Config Cache"
    print(Colors.FG.LightGreen + Colors.Bold + action + " Started" + Colors.Reset)
    shell.run_bash_command_popen(config, path, action,
                           "php -ddisplay_errors=on " + path + "/bin/magento setup:config:set --cache-backend=redis --cache-backend-redis-server=redis-config-cache --cache-backend-redis-db=0 --cache-backend-redis-port=6381", 1)

    action = "Configure Redis FPC"
    print(Colors.FG.LightGreen + Colors.Bold + action + " Started" + Colors.Reset)
    shell.run_bash_command_popen(config, path, action, "php -ddisplay_errors=on " + path + "/bin/magento setup:config:set --page-cache=redis --page-cache-redis-server=redis --page-cache-redis-db=0 --page-cache-redis-port=6379", 1)
    if menu_return == 1:
        menu.redis_menu(config, path)

