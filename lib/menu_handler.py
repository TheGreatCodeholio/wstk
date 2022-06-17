from lib.text_color import Colors
import lib.config_handler as conf
import lib.redis_handler as Redis
import lib.rabbitmq_handler as Rabbit
import lib.varnish_handler as Varnish
import lib.cron_handler as Cron
import lib.cache_handler as Cache
import lib.mysql_handler as Mysql
import sys


def main_menu(path):
    config = conf.load_config(path)
    choice = '0'
    while choice == '0':
        print(Colors.FG.Green + "+-----=> " + Colors.FG.Blue + "Stratus Toolkit Main Menu:" + Colors.FG.Green + " <=-----+" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 1. " + Colors.FG.Blue + "Redis" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 2. " + Colors.FG.Blue + "RabbitMQ" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 3. " + Colors.FG.Blue + "Varnish" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 4. " + Colors.FG.Blue + "Cron" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 5. " + Colors.FG.Blue + "Caches/Autoscaling" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 6. " + Colors.FG.Blue + "MySQL" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 7. " + Colors.FG.Blue + "Exit" + Colors.Reset)
        print(Colors.FG.Green + "+---------=> " + Colors.FG.Yellow + "Version 1.0" + Colors.FG.Green + "<=---------+" + Colors.Reset)

        choice = input(Colors.FG.Yellow + "Choose Menu Item: " + Colors.Reset)

        if choice == "7":
            sys.exit()
        elif choice == "6":
            mysql_menu(config, path)
        elif choice == "5":
            cache_menu(config, path)
        elif choice == "4":
            cron_menu(config, path)
        elif choice == "3":
            varnish_menu(config, path)
        elif choice == "2":
            rabbit_menu(config, path)
        elif choice == "1":
            redis_menu(config, path)
        else:
            print("I don't understand your choice.")


def redis_menu(config, path):
    choice = '0'
    while choice == '0':
        print(Colors.FG.Green + "++++++=> " + Colors.FG.Blue + "MMTK v1 Redis Menu:" + Colors.FG.Green + " <=++++++" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 1. " + Colors.FG.Blue + "Configure Redis Sessions" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 2. " + Colors.FG.Blue + "Configure Redis Cache" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 3. " + Colors.FG.Blue + "Back" + Colors.Reset)

        choice = input(Colors.FG.Yellow + "Choose Menu Item: " + Colors.Reset)

        if choice == "3":
            main_menu(path)
        elif choice == "2":
            Redis.config_cache(config, path)
        elif choice == "1":
            Redis.config_sessions(config, path)
        else:
            print("I don't understand your choice.")
            redis_menu(config, path)


def rabbit_menu(config, path):
    choice = '0'
    while choice == '0':
        print(Colors.FG.Green + "++++++=> " + Colors.FG.Blue + "MMTK v1 RabbitmQ Menu:" + Colors.FG.Green + " <=++++++" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 1. " + Colors.FG.Blue + "Configure RabbitMQ" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 2. " + Colors.FG.Blue + "Back" + Colors.Reset)

        choice = input(Colors.FG.Yellow + "Choose Menu Item: " + Colors.Reset)

        if choice == "2":
            main_menu(path)
        elif choice == "1":
            Rabbit.config_rabbitmq(config, path)
        else:
            print("I don't understand your choice.")
            rabbit_menu(config, path)


def varnish_menu(config, path):
    choice = '0'
    while choice == '0':
        print(Colors.FG.Green + "++++++=> " + Colors.FG.Blue + "MMTK v1 Varnish Menu:" + Colors.FG.Green + " <=++++++" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 1. " + Colors.FG.Blue + "Configure Varnish" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 2. " + Colors.FG.Blue + "Purge Varnish" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 3. " + Colors.FG.Blue + "Back" + Colors.Reset)

        choice = input(Colors.FG.Yellow + "Choose Menu Item: " + Colors.Reset)

        if choice == "3":
            main_menu(path)
        elif choice == "2":
            Varnish.purge_varnish(config, path)
        elif choice == "1":
            Varnish.config_varnish(config, path)
        else:
            print("I don't understand your choice.")
            varnish_menu(config, path)


def cron_menu(config, path):
    choice = '0'
    while choice == '0':
        print(Colors.FG.Green + "++++++=> " + Colors.FG.Blue + "MMTK v1 Cron Menu:" + Colors.FG.Green + " <=++++++" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 1. " + Colors.FG.Blue + "Install MageMojo Cron" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 2. " + Colors.FG.Blue + "Reset Crons" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 3. " + Colors.FG.Blue + "Back" + Colors.Reset)

        choice = input(Colors.FG.Yellow + "Choose Menu Item: " + Colors.Reset)

        if choice == "3":
            main_menu(path)
        elif choice == "2":
            Cron.reset_crons(config, path)
        elif choice == "1":
            Cron.install_mmcron(config, path)
        else:
            print("I don't understand your choice.")


def cache_menu(config, path):
    choice = '0'
    while choice == '0':
        print(Colors.FG.Green + "++++++=> " + Colors.FG.Blue + "MMTK v1 Cache Menu:" + Colors.FG.Green + " <=++++++" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 1. " + Colors.FG.Blue + "Clear All Cache" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 2. " + Colors.FG.Blue + "Clear Magento Cache" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 3. " + Colors.FG.Blue + "Clear Redis Cache" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 4. " + Colors.FG.Blue + "Clear Cloudfront Cache" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 5. " + Colors.FG.Blue + "Autoscaling Reinit" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 6. " + Colors.FG.Blue + "Back" + Colors.Reset)

        choice = input(Colors.FG.Yellow + "Choose Menu Item: " + Colors.Reset)

        if choice == "6":
            main_menu(path)
        elif choice == "5":
            Cache.reinit_as(config, path)
        elif choice == "4":
            Cache.clear_cloudfront(config, path)
        elif choice == "3":
            Cache.clear_redis(config, path)
        elif choice == "2":
            Cache.clear_magento(config, path)
        elif choice == "1":
            Cache.clear_all(config, path)

        else:
            print("I don't understand your choice.")
            redis_menu(config, path)


def mysql_menu(config, path):
    choice = '0'
    while choice == '0':
        print(Colors.FG.Green + "++++++=> " + Colors.FG.Blue + "MMTK v1 MySQL Menu:" + Colors.FG.Green + " <=++++++" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 1. " + Colors.FG.Blue + "Fix MySQL Credentials" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 2. " + Colors.FG.Blue + "Dump Database" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 3. " + Colors.FG.Blue + "Back" + Colors.Reset)

        choice = input(Colors.FG.Yellow + "Choose Menu Item: " + Colors.Reset)

        if choice == "3":
            main_menu(path)
        elif choice == "2":
            Mysql.mysql_dump(config, path)
        elif choice == "1":
            Mysql.fix_credentials(config, path)
        else:
            print("I don't understand your choice.")
            mysql_menu(config, path)