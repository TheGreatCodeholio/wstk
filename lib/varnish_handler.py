import lib.menu_handler as menu
import lib.command_handler as shell


def config_varnish(config, path):
    success_message = "Varnish Fully Configured"
    action = "Configure Varnish"
    shell.run_bash_command(config, path, action, "php " + path + "/bin/magento config:set system/full_page_cache/caching_application 2", "Set Full Page Cache to Varnish")
    shell.run_bash_command(config, path, action, "php " + path + "/bin/magento config:set system/full_page_cache/varnish/access_list localhost", "Set access list to localhost")
    shell.run_bash_command(config, path, action, "php " + path + "/bin/magento config:set system/full_page_cache/varnish/backend_host nginx", "Set backend host to NGINX")
    shell.run_bash_command(config, path, action, "php " + path + "/bin/magento config:set system/full_page_cache/varnish/backend_port 8080", "Set backend port to 8080")
    shell.run_bash_command(config, path, action, "php " + path + "/bin/magento setup:config:set --http-cache-hosts=varnish", success_message)
    menu.main_menu(path)


def purge_varnish(config, path):
    success_message = "Purged Varnish"
    action = "Purge Varnish"
    shell.run_bash_command(config, path, action, "curl -X 'PURGE' -H'X-Magento-Tags-Pattern: .*' varnish", success_message)
    menu.main_menu(path)
