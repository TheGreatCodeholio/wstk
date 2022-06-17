import lib.menu_handler as menu
from lib.text_color import Colors
import lib.config_handler as Conf


def config_sessions(config, path):
    if "save" in config["session"]:
        del config["session"]["save"]
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
    Conf.save_config(config, path)
    menu.main_menu(path)


def config_cache(config, path):
    if "cache" in config:
        del config["cache"]

    config["cache"] = {}
    config["cache"]["frontend"] = {}
    config["cache"]["frontend"]["default"] = {}
    config["cache"]["frontend"]["default"]["backend"] = "Cm_Cache_Backend_Redis"
    config["cache"]["frontend"]["default"]["backend_options"] = {}
    config["cache"]["frontend"]["default"]["backend_options"]["server"] = "redis-config-cache"
    config["cache"]["frontend"]["default"]["backend_options"]["database"] = "0"
    config["cache"]["frontend"]["default"]["backend_options"]["port"] = "6381"
    config["cache"]["frontend"]["page_cache"] = {}
    config["cache"]["frontend"]["page_cache"]["backend"] = "Cm_Cache_Backend_Redis"
    config["cache"]["frontend"]["page_cache"]["backend_options"] = {}
    config["cache"]["frontend"]["page_cache"]["backend_options"]["server"] = "redis"
    config["cache"]["frontend"]["page_cache"]["backend_options"]["port"] = "6379"
    config["cache"]["frontend"]["page_cache"]["backend_options"]["database"] = "1"
    config["cache"]["frontend"]["page_cache"]["backend_options"]["compress_data"] = "1"
    Conf.save_config(config, path)
    menu.main_menu(path)
