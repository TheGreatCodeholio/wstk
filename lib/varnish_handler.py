import lib.menu_handler as menu
import lib.command_handler as shell
import lib.config_handler as conf
from lib.text_color import Colors


def check_varnish(config, path):
    if "http_cache_hosts" not in config:
        config_varnish(config, path)
    elif "http_cache_hosts" in config:
        del config["http_cache_hosts"]
        conf.save_config(config, path)
        config_varnish(config, path)
    else:
        config_varnish(config, path)


def config_varnish(config, path):
    action = "Configure Varnish"
    shell.run_bash_command(config, path, action,
                           "php -ddisplay_errors=on " + path + "/bin/magento config:set system/full_page_cache/caching_application 2", ".")
    shell.run_bash_command(config, path, action,
                           "php -ddisplay_errors=on " + path + "/bin/magento config:set system/full_page_cache/varnish/access_list localhost",
                           "..")
    shell.run_bash_command(config, path, action,
                           "php -ddisplay_errors=on " + path + "/bin/magento config:set system/full_page_cache/varnish/backend_host nginx",
                           "...")
    shell.run_bash_command(config, path, action,
                           "php -ddisplay_errors=on " + path + "/bin/magento config:set system/full_page_cache/varnish/backend_port 8080",
                           "....")
    shell.run_bash_command(config, path, action,
                           "php -ddisplay_errors=on " + path + "/bin/magento setup:config:set --http-cache-hosts=varnish", ".....")
    print(Colors.FG.LightGreen + Colors.Bold + action + " Completed!" + Colors.Reset)
    menu.main_menu(path)


def purge_varnish(config, path):
    action = "Purge Varnish"
    shell.run_bash_command(config, path, action, "curl -X 'PURGE' -H'X-Magento-Tags-Pattern: .*' varnish", "...")
    print(Colors.FG.LightGreen + Colors.Bold + action + " Completed!" + Colors.Reset)
    menu.main_menu(path)
