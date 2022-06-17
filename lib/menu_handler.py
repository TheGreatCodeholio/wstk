from lib.text_color import Colors
import lib.config_handler as conf
import lib.redis_handler as Redis
import lib.rabbitmq_handler as Rabbit
import lib.varnish_handler as Varnish
import lib.cron_handler as Cron
import lib.cache_handler as Cache
import lib.mysql_handler as Mysql
import lib.elasticsearch_handler as ElasticSearch
import sys
version = "1.0"

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
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 7. " + Colors.FG.Blue + "ElasticSearch" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 9. " + Colors.FG.Blue + "Exit" + Colors.Reset)
        print(Colors.FG.Green + "+---------=> " + Colors.FG.Yellow + "Version " + version + " " + Colors.FG.Green + "<=---------+" + Colors.Reset)

        choice = input(Colors.FG.Yellow + "Choose Menu Item: " + Colors.Reset)

        if choice == "8":
            sys.exit()
        elif choice == "6":
            elasticsearch_menu(config, path)
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
            print(Colors.FG.Red + Colors.Bold + "Invalid menu choice." + Colors.Reset)
            main_menu(path)

def redis_menu(config, path):
    choice = '0'
    while choice == '0':
        print(Colors.FG.Green + "++++++=> " + Colors.FG.Blue + "Redis Menu:" + Colors.FG.Green + " <=++++++" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 1. " + Colors.FG.Blue + "Configure Redis Sessions" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 2. " + Colors.FG.Blue + "Configure Redis Cache" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 3. " + Colors.FG.Blue + "Back" + Colors.Reset)
        print(Colors.FG.Green + "+---------=> " + Colors.FG.Yellow + "Version " + version + " " + Colors.FG.Green + "<=---------+" + Colors.Reset)

        choice = input(Colors.FG.Yellow + "Choose Menu Item: " + Colors.Reset)

        if choice == "3":
            main_menu(path)
        elif choice == "2":
            Redis.config_cache(config, path)
        elif choice == "1":
            Redis.config_sessions(config, path)
        else:
            print(Colors.FG.Red + Colors.Bold + "Invalid menu choice." + Colors.Reset)
            redis_menu(config, path)


def rabbit_menu(config, path):
    choice = '0'
    while choice == '0':
        print(Colors.FG.Green + "++++++=> " + Colors.FG.Blue + "RabbitmQ Menu:" + Colors.FG.Green + " <=++++++" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 1. " + Colors.FG.Blue + "Configure RabbitMQ" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 2. " + Colors.FG.Blue + "Back" + Colors.Reset)
        print(Colors.FG.Green + "+---------=> " + Colors.FG.Yellow + "Version " + version + " " + Colors.FG.Green + "<=---------+" + Colors.Reset)

        choice = input(Colors.FG.Yellow + "Choose Menu Item: " + Colors.Reset)

        if choice == "2":
            main_menu(path)
        elif choice == "1":
            Rabbit.check_rabbitmq(config, path)
        else:
            print(Colors.FG.Red + Colors.Bold + "Invalid menu choice." + Colors.Reset)
            rabbit_menu(config, path)


def varnish_menu(config, path):
    choice = '0'
    while choice == '0':
        print(Colors.FG.Green + "++++++=> " + Colors.FG.Blue + "Varnish Menu:" + Colors.FG.Green + " <=++++++" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 1. " + Colors.FG.Blue + "Configure Varnish" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 2. " + Colors.FG.Blue + "Purge Varnish" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 3. " + Colors.FG.Blue + "Back" + Colors.Reset)
        print(Colors.FG.Green + "+---------=> " + Colors.FG.Yellow + "Version " + version + " " + Colors.FG.Green + "<=---------+" + Colors.Reset)

        choice = input(Colors.FG.Yellow + "Choose Menu Item: " + Colors.Reset)

        if choice == "3":
            main_menu(path)
        elif choice == "2":
            Varnish.purge_varnish(config, path)
        elif choice == "1":
            Varnish.check_varnish(config, path)
        else:
            print(Colors.FG.Red + Colors.Bold + "Invalid menu choice." + Colors.Reset)
            varnish_menu(config, path)


def cron_menu(config, path):
    choice = '0'
    while choice == '0':
        print(Colors.FG.Green + "++++++=> " + Colors.FG.Blue + "Cron Menu:" + Colors.FG.Green + " <=++++++" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 1. " + Colors.FG.Blue + "Install MageMojo Cron" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 2. " + Colors.FG.Blue + "Reset Crons" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 3. " + Colors.FG.Blue + "Back" + Colors.Reset)
        print(Colors.FG.Green + "+---------=> " + Colors.FG.Yellow + "Version " + version + " " + Colors.FG.Green + "<=---------+" + Colors.Reset)

        choice = input(Colors.FG.Yellow + "Choose Menu Item: " + Colors.Reset)

        if choice == "3":
            main_menu(path)
        elif choice == "2":
            Cron.reset_crons(config, path)
        elif choice == "1":
            Cron.install_mmcron(config, path)
        else:
            print(Colors.FG.Red + Colors.Bold + "Invalid menu choice." + Colors.Reset)
            cron_menu(config, path)


def cache_menu(config, path):
    choice = '0'
    while choice == '0':
        print(Colors.FG.Green + "++++++=> " + Colors.FG.Blue + "Cache Menu:" + Colors.FG.Green + " <=++++++" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 1. " + Colors.FG.Blue + "Clear All Cache" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 2. " + Colors.FG.Blue + "Clear Magento Cache" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 3. " + Colors.FG.Blue + "Clear Redis Cache" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 4. " + Colors.FG.Blue + "Clear Cloudfront Cache" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 5. " + Colors.FG.Blue + "Autoscaling Reinit" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 6. " + Colors.FG.Blue + "Back" + Colors.Reset)
        print(Colors.FG.Green + "+---------=> " + Colors.FG.Yellow + "Version " + version + " " + Colors.FG.Green + "<=---------+" + Colors.Reset)

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
            print(Colors.FG.Red + Colors.Bold + "Invalid menu choice." + Colors.Reset)
            redis_menu(config, path)


def mysql_menu(config, path):
    choice = '0'
    while choice == '0':
        print(Colors.FG.Green + "++++++=> " + Colors.FG.Blue + "MySQL Menu:" + Colors.FG.Green + " <=++++++" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 1. " + Colors.FG.Blue + "Update MySQL Credentials Auto" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 2. " + Colors.FG.Blue + "Update MySQL Credentials Manual" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 3. " + Colors.FG.Blue + "Backup Database Auto" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 4. " + Colors.FG.Blue + "Backup Database Manual" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 5. " + Colors.FG.Blue + "Back" + Colors.Reset)
        print(Colors.FG.Green + "+---------=> " + Colors.FG.Yellow + "Version " + version + " " + Colors.FG.Green + "<=---------+" + Colors.Reset)

        choice = input(Colors.FG.Yellow + "Choose Menu Item: " + Colors.Reset)

        if choice == "5":
            main_menu(path)
        elif choice == "4":
            Mysql.mysql_dump_manual(config, path)
        elif choice == "3":
            Mysql.mysql_dump_auto(config, path, "/srv/backups")
        elif choice == "2":
            Mysql.update_mysql_credentials_manual(config, path)
        elif choice == "1":
            Mysql.update_mysql_credentials_from_system(config, path)
        else:
            print(Colors.FG.Red + Colors.Bold + "Invalid menu choice." + Colors.Reset)
            mysql_menu(config, path)

def elasticsearch_menu(config, path):
    choice = '0'
    while choice == '0':
        print(Colors.FG.Green + "++++++=> " + Colors.FG.Blue + "Elasticsearch Menu:" + Colors.FG.Green + " <=++++++" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 1. " + Colors.FG.Blue + "Configure Elasticsearch" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 2. " + Colors.FG.Blue + "Reindex Search Catalog" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 3. " + Colors.FG.Blue + "Back" + Colors.Reset)
        print(Colors.FG.Green + "+---------=> " + Colors.FG.Yellow + "Version " + version + " " + Colors.FG.Green + "<=---------+" + Colors.Reset)

        choice = input(Colors.FG.Yellow + "Choose Menu Item: " + Colors.Reset)

        if choice == "3":
            main_menu(path)
        elif choice == "2":
            ElasticSearch.reindex_elasticsearch(config, path)
        elif choice == "1":
            ElasticSearch.configure_elasticsearch(config, path)
        else:
            print(Colors.FG.Red + Colors.Bold + "Invalid menu choice." + Colors.Reset)
            cron_menu(config, path)