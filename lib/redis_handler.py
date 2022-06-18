import lib.menu_handler as menu
from lib.text_color import Colors
import lib.command_handler as shell
import lib.config_handler as conf


def check_redis_sessions(config, path):
    if "save" not in config:
        config_sessions(config, path)
    elif "save" in config:
        del config["save"]
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
    print(Colors.FG.LightGreen + Colors.Bold + action + " Started" + Colors.Reset)
    config["session"] = {}
    config["session"]["save"] = "redis"
    config["session"]["redis"] = {}
    config["session"]["redis"]["host"] = "redis-session"
    config["session"]["redis"]["port"] = "6380"
    config["session"]["redis"]["password"] = ""
    config["session"]["redis"]["timeout"] = "2.5"
    config["session"]["redis"]["persistent_identifier"] = ""
    config["session"]["redis"]["database"] = "2"
    config["session"]["redis"]["compression_threshold"] = "2048"
    config["session"]["redis"]["compression_library"] = "gzip"
    config["session"]["redis"]["log_level"] = "1"
    config["session"]["redis"]["max_concurrency"] = "20"
    config["session"]["redis"]["break_after_frontend"] = "5"
    config["session"]["redis"]["break_after_adminhtml"] = "30"
    config["session"]["redis"]["first_lifetime"] = "600"
    config["session"]["redis"]["bot_first_lifetime"] = "60"
    config["session"]["redis"]["bot_lifetime"] = "7200"
    config["session"]["redis"]["disable_locking"] = "1"
    config["session"]["redis"]["min_lifetime"] = "60"
    config["session"]["redis"]["max_lifetime"] = "2592000"
    conf.save_config(config, path)
    print(Colors.FG.LightGreen + Colors.Bold + action + " Completed!" + Colors.Reset)
    menu.main_menu(path)


def config_cache(config, path):
    action = "Configure Redis FPC and Cache"
    print(Colors.FG.LightGreen + Colors.Bold + action + " Started" + Colors.Reset)
    config["cache"] = {}
    config["cache"]["frontend"] = {}
    config["cache"]["frontend"]["default"] = {}
    config["cache"]["frontend"]["default"]["backend"] = "Magento\\Framework\\Cache\\Backend\\Redis"
    config["cache"]["frontend"]["default"]["backend_options"] = {}
    config["cache"]["frontend"]["default"]["backend_options"]["server"] = "redis-config-cache"
    config["cache"]["frontend"]["default"]["backend_options"]["database"] = "0"
    config["cache"]["frontend"]["default"]["backend_options"]["port"] = "6381"
    config["cache"]["frontend"]["page_cache"] = {}
    config["cache"]["frontend"]["page_cache"]["backend"] = "Magento\\Framework\\Cache\\Backend\\Redis"
    config["cache"]["frontend"]["page_cache"]["backend_options"] = {}
    config["cache"]["frontend"]["page_cache"]["backend_options"]["server"] = "redis"
    config["cache"]["frontend"]["page_cache"]["backend_options"]["port"] = "6379"
    config["cache"]["frontend"]["page_cache"]["backend_options"]["database"] = "1"
    config["cache"]["frontend"]["page_cache"]["backend_options"]["compress_data"] = "1"
    config["cache"]["allow_parallel_generation"] = False
    conf.save_config(config, path)
    print(Colors.FG.LightGreen + Colors.Bold + action + " Completed!" + Colors.Reset)
    menu.main_menu(path)