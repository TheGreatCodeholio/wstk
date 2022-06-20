import lib.menu_handler as menu
import lib.command_handler as shell
import lib.config_handler as conf
from lib.text_color import Colors


def check_varnish(config, path, menu_return):
    if "http_cache_hosts" not in config:
        config_varnish(config, path, menu_return)
    elif "http_cache_hosts" in config:
        del config["http_cache_hosts"]
        conf.save_config(config, path)
        config_varnish(config, path, menu_return)
    else:
        config_varnish(config, path, menu_return)


def config_varnish(config, path, menu_return):
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
    if menu_return == 1:
        menu.varnish_menu(config, path)


def purge_varnish(config, path, menu_return):
    action = "Purge Varnish"
    shell.run_bash_command(config, path, action, "curl -X 'PURGE' -H'X-Magento-Tags-Pattern: .*' varnish", "...")
    print(Colors.FG.LightGreen + Colors.Bold + action + " Completed!" + Colors.Reset)
    if menu_return == 1:
        menu.varnish_menu(config, path)
