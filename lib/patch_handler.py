from lib.text_color import Colors
import lib.command_handler as shell
import lib.composer_handler as composer
import lib.magento_handler as magento
import lib.menu_handler as menu
import json


def install_catalog_rabbitmq(config, path, menu_return):
    """Patch to convert product_action_attribute.update and product_action_attribute.website.update consumers from
    MySQL to RabbitMQ Broker """

    composer.install_cweagans(config, path)
    composer_config = composer.load_composer_json(config, path)
    if composer_config:
        if "extra" in composer_config:
            if "patches" in composer_config["extra"]:
                if "magento/module-catalog" in composer_config["extra"]["patches"]:
                    print("Already Installed.")
                    menu.magento_patch_menu(config, path)
                else:
                    composer_config["extra"]["patches"]["magento/module-catalog"] = {
                        "Catalog-RabbitMQ: product_action_attribute.update and product_action_attribute.website.update conversion to amqp": "https://raw.githubusercontent.com/magemojo/m2-patches/main/module-catalog.patch"}
                    composer.save_composer_json(config, path, composer_config)
            else:
                composer_config["extra"]["patches"] = {}
                composer_config["extra"]["patches"]["magento/module-catalog"] = {
                    "Catalog-RabbitMQ: product_action_attribute.update and product_action_attribute.website.update conversion to amqp": "https://raw.githubusercontent.com/magemojo/m2-patches/main/module-catalog.patch"}
                composer.save_composer_json(config, path, composer_config)
        else:
            composer_config["extra"] = {}
            composer_config["extra"]["patches"] = {}
            composer_config["extra"]["patches"]["magento/module-catalog"] = {
                "Catalog-RabbitMQ: product_action_attribute.update and product_action_attribute.website.update conversion to amqp": "https://raw.githubusercontent.com/magemojo/m2-patches/main/module-catalog.patch"}
            composer.save_composer_json(config, path, composer_config)
    else:
        print(path + "/composer.json seems to be empty")

    composer.composer_install(config, path)
    composer.composer_lock(config, path)
    magento.magento_setup_upgrade(config, path)
    magento.magento_compile(config, path)
    magento.static_content_deploy(config, path)
    if menu_return == 1:
        menu.magento_patch_menu(config, path)


def install_pdo_adapter_mysql8(config, path, menu_return):
    """ Patch to fix PDO Adapter when MySQL 8.0 used for Temporary tables using LIKE SQL query.
    According to MySQL doc pages: https://dev.mysql.com/doc/refman/8.0/en/create-temporary-table.html """

    composer.install_cweagans(config, path)
    composer_config = composer.load_composer_json(config, path)
    if composer_config:
        if "extra" in composer_config:
            if "patches" in composer_config["extra"]:
                if "magento/framework" in composer_config["extra"]["patches"]:
                    print("Already Installed.")
                    menu.magento_patch_menu(config, path)
                else:
                    composer_config["extra"]["patches"]["magento/framework"] = {
                        "Magento2-Framework-PDO-Adapter-MySQL8: Patch to fix PDO Adapter when MySQL 8.0 used for Temporary tables using LIKE SQL query": "https://raw.githubusercontent.com/magemojo/m2-patches/main/framework-adapter-pdo.patch"}
                    composer.save_composer_json(config, path, composer_config)
            else:
                composer_config["extra"]["patches"] = {}
                composer_config["extra"]["patches"]["magento/framework"] = {
                    "Magento2-Framework-PDO-Adapter-MySQL8: Patch to fix PDO Adapter when MySQL 8.0 used for Temporary tables using LIKE SQL query": "https://raw.githubusercontent.com/magemojo/m2-patches/main/framework-adapter-pdo.patch"}
                composer.save_composer_json(config, path, composer_config)
        else:
            composer_config["extra"] = {}
            composer_config["extra"]["patches"] = {}
            composer_config["extra"]["patches"]["magento/framework"] = {
                "Magento2-Framework-PDO-Adapter-MySQL8: Patch to fix PDO Adapter when MySQL 8.0 used for Temporary tables using LIKE SQL query": "https://raw.githubusercontent.com/magemojo/m2-patches/main/framework-adapter-pdo.patch"}
            composer.save_composer_json(config, path, composer_config)
    else:
        print(path + "/composer.json seems to be empty")

    composer.composer_install(config, path)
    composer.composer_lock(config, path)
    magento.magento_setup_upgrade(config, path)
    magento.magento_compile(config, path)
    magento.static_content_deploy(config, path)
    if menu_return == 1:
        menu.magento_patch_menu(config, path)
