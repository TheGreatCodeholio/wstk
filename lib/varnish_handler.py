import lib.menu_handler as Menu
from lib.text_color import Colors
import lib.config_handler as Conf
import os

def config_varnish(config, path):
    os.popen("php " + path + "/bin/magento config:set system/full_page_cache/caching_application 2")
    os.popen("php " + path + "/bin/magento config:set system/full_page_cache/varnish/access_list localhost")
    os.popen("php " + path + "/bin/magento config:set system/full_page_cache/varnish/backend_host nginx")
    os.popen("php " + path + "/bin/magento config:set system/full_page_cache/varnish/backend_port 8080")
    os.popen("php " + path + "/bin/magento setup:config:set --http-cache-hosts=varnish")
    print(Colors.OKGREEN + "Configured Varnish")
    Menu.main_menu(config, path)

def purge_varnish(config, path):
    os.popen("curl -X 'PURGE' -H'X-Magento-Tags-Pattern: .*' varnish")
    print(Colors.OKGREEN + "Purged Varnish")
    Menu.main_menu(config, path)
