import lib.menu_handler as menu
from lib.text_color import Colors
import lib.command_handler as shell
import lib.magento_handler as mage


def configure_elasticsearch(config, path, menu_return):
    action = "Configure Database for Elastic Search"
    version = input("ElasticSearch version? 5, 6 or 7 (Default 7):")
    if version == "":
        version = "elasticsearch7"
    elif version == "5":
        version = "elasticsearch5"
    elif version == "6":
        version = "elasticsearch6"
    elif version == "7":
        version = "elasticsearch7"
    else:
        print(Colors.FG.Yellow + "Versions can only be 5, 6, or 7: " + version + Colors.Reset)
        menu.main_menu(path)

    shell.run_bash_command(config, path, action,
                           "php -ddisplay_errors=on " + path + "/bin/magento config:set catalog/search/engine " + version,
                           ".")
    shell.run_bash_command(config, path, action,
                           "php -ddisplay_errors=on " + path + "/bin/magento config:set catalog/search/" + version + "_server_hostname elasticsearch",
                           "..")
    shell.run_bash_command(config, path, action,
                           "php -ddisplay_errors=on " + path + "/bin/magento config:set catalog/search/" + version + "_server_port 9200",
                           "...")
    shell.run_bash_command(config, path, action,
                           "php -ddisplay_errors=on " + path + "/bin/magento config:set catalog/search/" + version + "_index_prefix magento2",
                           "....")
    shell.run_bash_command(config, path, action,
                           "php -ddisplay_errors=on " + path + "/bin/magento config:set catalog/search/" + version + "_enable_auth 0",
                           ".....")
    shell.run_bash_command(config, path, action,
                           "php -ddisplay_errors=on " + path + "/bin/magento config:set catalog/search/" + version + "_server_timeout 15",
                           "......")
    print(Colors.FG.LightGreen + Colors.Bold + action + " Completed." + Colors.Reset)

    action = "Reindex Search Catalog"
    print(Colors.FG.LightGreen + Colors.Bold + action + " Started." + Colors.Reset)
    shell.run_bash_command(config, path, action,
                           "php -ddisplay_errors=on " + path + "/bin/magento indexer:reindex catalogsearch_fulltext",
                           ".......")
    print(Colors.FG.LightGreen + Colors.Bold + action + " Completed." + Colors.Reset)
    print(Colors.FG.LightGreen + Colors.Bold + "ElasticSearch Configured" + Colors.Reset)
    if menu_return == 1:
        menu.elasticsearch_menu(config, path)


def reindex_elasticsearch(config, path, menu_return):
    mage.reindex_one_index(config, path, "catalogsearch_fulltext")
    if menu_return == 1:
        menu.elasticsearch_menu(config, path)