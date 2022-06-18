import lib.menu_handler as menu
from lib.text_color import Colors
import lib.config_handler as conf
import lib.command_handler as shell
from subprocess import check_output


def check_rabbitmq(config, path):
    if "queue" not in config:
        config_rabbitmq(config, path)
    elif "amqp" in config["queue"]:
        del config["queue"]
        conf.save_config(config, path)
        config_rabbitmq(config, path)
    else:
        config_rabbitmq(config, path)


def config_rabbitmq(config, path):
    action = "RabbitMQ Configuration"
    rabbit_password = input(Colors.FG.Yellow + "RabbitMQ Password:" + Colors.Reset)
    shell.run_bash_command(config, path, action, "php -ddisplay_errors=on " + path + "/bin/magento setup:config:set --amqp-host=rabbitmq --amqp-port=5672 --amqp-user=username --amqp-password=" + rabbit_password + " --amqp-virtualhost=/", "..")

    consumers = check_output(['php', path + '/bin/magento', 'queue:consumers:list'])

    config = conf.load_config(path)
    if "cron_consumers_runner" in config:
        del config["cron_consumers_runner"]
    config["cron_consumers_runner"] = {}
    config["cron_consumers_runner"]["cron_run"] = "True"
    config["cron_consumers_runner"]["max_messages"] = 0
    config["cron_consumers_runner"]["consumers"] = consumers.decode("utf-8").splitlines()
    conf.save_config(config, path)
    print(Colors.FG.LightGreen + Colors.Bold + action + " Completed!" + Colors.Reset)
    menu.main_menu(path)
