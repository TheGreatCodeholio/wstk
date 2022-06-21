import lib.menu_handler as menu
from lib.text_color import Colors
import lib.config_handler as conf
import lib.command_handler as shell
from subprocess import check_output


def check_rabbitmq(config, path, menu_return):
    if "queue" not in config:
        config_rabbitmq(config, path, menu_return)
    elif "amqp" in config["queue"]:
        del config["queue"]
        conf.save_config(config, path)
        config_rabbitmq(config, path, menu_return)
    else:
        config_rabbitmq(config, path, menu_return)


def config_rabbitmq(config, path, menu_return):
    action = "RabbitMQ Configuration"
    config = conf.load_config(path)
    rabbit_password = input(Colors.FG.Yellow + "RabbitMQ Password:" + Colors.Reset)
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
    conf.save_config(config, path)
    print(Colors.FG.LightGreen + Colors.Bold + action + " Completed!" + Colors.Reset)
    if menu_return == 1:
        menu.rabbit_menu(config, path)
