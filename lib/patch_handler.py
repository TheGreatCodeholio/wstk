from lib.text_color import Colors
import lib.command_handler as shell
import lib.composer_handler as composer
import lib.magento_handler as magento
import lib.menu_handler as menu
import json


def install_catalog_rabbitmq(config, path):
    """Patch to convert product_action_attribute.update and product_action_attribute.website.update consumers from
    MySQL to RabbitMQ Broker """

    composer.install_cweagans(config, path)
    composer_config = composer.load_composer_json(config, path)
    if composer_config:
        if "extras" in composer_config:
            if "patches" in composer_config["extras"]:
                if "magento/module-catalog" in composer_config["extras"]["patches"]:
                    print("Already Installed.")
                    menu.magento_patch_menu(config, path)
                else:
                    composer_config["extras"]["patches"]["magento/module-catalog"] = { "Catalog-RabbitMQ: product_action_attribute.update and product_action_attribute.website.update conversion to amqp": "https://raw.githubusercontent.com/magemojo/m2-patches/main/module-catalog.patch"}
                    composer.save_composer_json(config, path, composer_config)
            else:
                composer_config["extras"]["patches"] = {}
                composer_config["extras"]["patches"]["magento/module-catalog"] = {
                    "Catalog-RabbitMQ: product_action_attribute.update and product_action_attribute.website.update conversion to amqp": "https://raw.githubusercontent.com/magemojo/m2-patches/main/module-catalog.patch"}
                composer.save_composer_json(config, path, composer_config)
        else:
            composer_config["extras"] = {}
            composer_config["extras"]["patches"] = {}
            composer_config["extras"]["patches"]["magento/module-catalog"] = {
                "Catalog-RabbitMQ: product_action_attribute.update and product_action_attribute.website.update conversion to amqp": "https://raw.githubusercontent.com/magemojo/m2-patches/main/module-catalog.patch"}
            composer.save_composer_json(config, path, composer_config)
    else:
        print(path + "/composer.json seems to be empty")

    composer.composer_install(config, path)
    composer.composer_lock(config, path)
    magento.magento_setup_upgrade(config, path)
    magento.magento_compile(config, path)
    magento.static_content_deploy(config, path)
    menu.magento_patch_menu(config, path)