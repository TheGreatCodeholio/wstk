from lib.text_color import Colors
import lib.redis_handler as Redis
import lib.rabbitmq_handler as Rabbit
import lib.varnish_handler as Varnish
import lib.cron_handler as Cron

def main_menu(config, path):
    choice = '0'
    while choice == '0':
        print(Colors.OKGREEN + "++++++=> " + Colors.OKBLUE + "MMTK v1 Main Menu:" + Colors.OKGREEN + " <=++++++" + Colors.ENDC)
        print(Colors.OKGREEN + "=>" + Colors.WARNING + " 1. " + Colors.OKBLUE + "Redis" + Colors.ENDC)
        print(Colors.OKGREEN + "=>" + Colors.WARNING + " 2. " + Colors.OKBLUE + "RabbitMQ" + Colors.ENDC)
        print(Colors.OKGREEN + "=>" + Colors.WARNING + " 3. " + Colors.OKBLUE + "Varnish" + Colors.ENDC)
        print(Colors.OKGREEN + "=>" + Colors.WARNING + " 4. " + Colors.OKBLUE + "Cron" + Colors.ENDC)

        choice = input(Colors.WARNING + "Choose Menu Item: " + Colors.ENDC)

        if choice == "4":
            print("Do Something 4")
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
        print(Colors.OKGREEN + "++++++=> " + Colors.OKBLUE + "MMTK v1 Redis Menu:" + Colors.OKGREEN + " <=++++++" + Colors.ENDC)
        print(Colors.OKGREEN + "=>" + Colors.WARNING + " 1. " + Colors.OKBLUE + "Configure Redis Sessions" + Colors.ENDC)
        print(Colors.OKGREEN + "=>" + Colors.WARNING + " 2. " + Colors.OKBLUE + "Configure Redis Cache" + Colors.ENDC)
        print(Colors.OKGREEN + "=>" + Colors.WARNING + " 3. " + Colors.OKBLUE + "Back" + Colors.ENDC)

        choice = input(Colors.WARNING + "Choose Menu Item: " + Colors.ENDC)

        if choice == "3":
            main_menu(config, path)
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
        print(Colors.OKGREEN + "++++++=> " + Colors.OKBLUE + "MMTK v1 RabbitmQ Menu:" + Colors.OKGREEN + " <=++++++" + Colors.ENDC)
        print(Colors.OKGREEN + "=>" + Colors.WARNING + " 1. " + Colors.OKBLUE + "Configure RabbitMQ" + Colors.ENDC)
        print(Colors.OKGREEN + "=>" + Colors.WARNING + " 2. " + Colors.OKBLUE + "Back" + Colors.ENDC)

        choice = input(Colors.WARNING + "Choose Menu Item: " + Colors.ENDC)

        if choice == "2":
            main_menu(config, path)
        elif choice == "1":
            Rabbit.check_rabbitmq(config, path)
        else:
            print("I don't understand your choice.")
            rabbit_menu(config, path)


def varnish_menu(config, path):
    choice = '0'
    while choice == '0':
        print(Colors.OKGREEN + "++++++=> " + Colors.OKBLUE + "MMTK v1 Varnish Menu:" + Colors.OKGREEN + " <=++++++" + Colors.ENDC)
        print(Colors.OKGREEN + "=>" + Colors.WARNING + " 1. " + Colors.OKBLUE + "Configure Varnish" + Colors.ENDC)
        print(Colors.OKGREEN + "=>" + Colors.WARNING + " 2. " + Colors.OKBLUE + "Purge Varnish" + Colors.ENDC)
        print(Colors.OKGREEN + "=>" + Colors.WARNING + " 3. " + Colors.OKBLUE + "Back" + Colors.ENDC)

        choice = input(Colors.WARNING + "Choose Menu Item: " + Colors.ENDC)

        if choice == "3":
            main_menu(config, path)
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
        print(Colors.OKGREEN + "++++++=> " + Colors.OKBLUE + "MMTK v1 Cron Menu:" + Colors.OKGREEN + " <=++++++" + Colors.ENDC)
        print(Colors.OKGREEN + "=>" + Colors.WARNING + " 1. " + Colors.OKBLUE + "Install MageMojo Cron" + Colors.ENDC)
        print(Colors.OKGREEN + "=>" + Colors.WARNING + " 2. " + Colors.OKBLUE + "Reset Crons" + Colors.ENDC)
        print(Colors.OKGREEN + "=>" + Colors.WARNING + " 3. " + Colors.OKBLUE + "Back" + Colors.ENDC)

        choice = input(Colors.WARNING + "Choose Menu Item: " + Colors.ENDC)

        if choice == "3":
            main_menu(config, path)
        elif choice == "2":
            Cron.reset_crons(config, path)
        elif choice == "1":
            Cron.install_mmcron(config, path)
        else:
            print("I don't understand your choice.")