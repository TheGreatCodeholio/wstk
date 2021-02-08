import lib.menu_handler as Menu
from lib.text_color import Colors
import lib.config_handler as Conf
from subprocess import check_output


def check_rabbitmq(config, path):
    if "queue" not in config:
        config_rabbitmq(config, path)
    elif "amqp" in config["queue"]:
        print(Colors.OKGREEN + "RabbitMQ Already Configured" + Colors.ENDC)
        Menu.main_menu(config, path)
    else:
        config_rabbitmq(config, path)


def config_rabbitmq(config, path):
    rabbit_password = input(Colors.WARNING + "RabbitMQ Password:" + Colors.ENDC)
    if "queue" in config:
        del config["queue"]
    config["queue"] = {}
    config["queue"]["amqp"] = {}
    config["queue"]["amqp"]["host"] = "rabbitmq"
    config["queue"]["amqp"]["port"] = "5672"
    config["queue"]["amqp"]["user"] = "username"
    config["queue"]["amqp"]["password"] = rabbit_password
    config["queue"]["amqp"]["virtualhost"] = "/"
    config["queue"]["amqp"]["ssl"] = "false"
    config["queue"]["amqp"]["ssl_options"] = {}

    consumers = check_output(['php', path + '/bin/magento', 'queue:consumers:list'])

    if "cron_consumers_runner" in config:
        del config["cron_consumers_runner"]
    config["cron_consumers_runner"] = {}
    config["cron_consumers_runner"]["cron_run"] = "True"
    config["cron_consumers_runner"]["max_messages"] = 0
    config["cron_consumers_runner"]["consumers"] = consumers.decode("utf-8").splitlines()
    Conf.save_config(config, path)
    Menu.main_menu(config, path)
