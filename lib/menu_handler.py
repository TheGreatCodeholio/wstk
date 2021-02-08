import lib.text_color as Color
import lib.redis_handler as Redis
import lib.rabbitmq_handler as Rabbit
import lib.varnish_handler as Varnish


def main_menu(config, path):
    choice = '0'
    while choice == '0':
        print(
            Color.Colors.OKGREEN + "++++++=> " + Color.Colors.OKBLUE + "MMTK v1 Main Menu:" + Color.Colors.OKGREEN + " <=++++++" + Color.Colors.ENDC)
        print(
            Color.Colors.OKGREEN + "=>" + Color.Colors.WARNING + " 1. " + Color.Colors.OKBLUE + "Redis" + Color.Colors.ENDC)
        print(
            Color.Colors.OKGREEN + "=>" + Color.Colors.WARNING + " 2. " + Color.Colors.OKBLUE + "RabbitMQ" + Color.Colors.ENDC)
        print(
            Color.Colors.OKGREEN + "=>" + Color.Colors.WARNING + " 3. " + Color.Colors.OKBLUE + "Varnish" + Color.Colors.ENDC)
        print(
            Color.Colors.OKGREEN + "=>" + Color.Colors.WARNING + " 4. " + Color.Colors.OKBLUE + "Cron" + Color.Colors.ENDC)

        choice = input(Color.Colors.WARNING + "Choose Menu Item: ")

        if choice == "4":
            print("Do Something 4")
        elif choice == "3":
            print("Do Something 2")
        elif choice == "2":
            rabbit_menu(config, path)
        elif choice == "1":
            redis_menu(config, path)
        else:
            print("I don't understand your choice.")


def redis_menu(config, path):
    choice = '0'
    while choice == '0':
        print(
            Color.Colors.OKGREEN + "++++++=> " + Color.Colors.OKBLUE + "MMTK v1 Redis Menu:" + Color.Colors.OKGREEN + " <=++++++" + Color.Colors.ENDC)
        print(
            Color.Colors.OKGREEN + "=>" + Color.Colors.WARNING + " 1. " + Color.Colors.OKBLUE + "Configure Redis Sessions" + Color.Colors.ENDC)
        print(
            Color.Colors.OKGREEN + "=>" + Color.Colors.WARNING + " 2. " + Color.Colors.OKBLUE + "Configure Redis Cache" + Color.Colors.ENDC)
        print(
            Color.Colors.OKGREEN + "=>" + Color.Colors.WARNING + " 3. " + Color.Colors.OKBLUE + "Back" + Color.Colors.ENDC)

        choice = input("Choose Menu Item: ")

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
        print(
            Color.Colors.OKGREEN + "++++++=> " + Color.Colors.OKBLUE + "MMTK v1 RabbitmQ Menu:" + Color.Colors.OKGREEN + " <=++++++" + Color.Colors.ENDC)
        print(
            Color.Colors.OKGREEN + "=>" + Color.Colors.WARNING + " 1. " + Color.Colors.OKBLUE + "Configure RabbitMQ" + Color.Colors.ENDC)
        print(
            Color.Colors.OKGREEN + "=>" + Color.Colors.WARNING + " 2. " + Color.Colors.OKBLUE + "Back" + Color.Colors.ENDC)

        choice = input("Choose Menu Item: ")

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
        print(
            Color.Colors.OKGREEN + "++++++=> " + Color.Colors.OKBLUE + "MMTK v1 Varnish Menu:" + Color.Colors.OKGREEN + " <=++++++" + Color.Colors.ENDC)
        print(
            Color.Colors.OKGREEN + "=>" + Color.Colors.WARNING + " 1. " + Color.Colors.OKBLUE + "Configure Varnish" + Color.Colors.ENDC)
        print(
            Color.Colors.OKGREEN + "=>" + Color.Colors.WARNING + " 2. " + Color.Colors.OKBLUE + "Purge Varnish" + Color.Colors.ENDC)
        print(
            Color.Colors.OKGREEN + "=>" + Color.Colors.WARNING + " 3. " + Color.Colors.OKBLUE + "Back" + Color.Colors.ENDC)

        choice = input("Choose Menu Item: ")

        if choice == "3":
            main_menu(config, path)
        elif choice == "2":
            Varnish.purge_varnish(config, path)
        elif choice == "1":
            Varnish.config_varnish(config, path)
        else:
            print("I don't understand your choice.")
            varnish_menu(config, path)
