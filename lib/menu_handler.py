from lib.text_color import Colors
import lib.config_handler as conf
import lib.redis_handler as Redis
import lib.rabbitmq_handler as Rabbit
import lib.varnish_handler as Varnish
import lib.cron_handler as Cron
import lib.cache_handler as Cache
import lib.mysql_handler as Mysql
import lib.magento_handler as Magento
import lib.elasticsearch_handler as ElasticSearch
import lib.patch_handler as Patches
import lib.backup_handler as Backup
import lib.dev_copy_handler as Dev
import sys
version = "1.0"

def main_menu(path):
    config = conf.load_config(path)
    choice = '0'
    while choice == '0':
        print(Colors.FG.Green + "+-----=> " + Colors.FG.LightBlue + "Stratus Toolkit Main Menu:" + Colors.FG.Green + " <=-----+" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 1. " + Colors.FG.LightBlue + "Magento" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 2. " + Colors.FG.LightBlue + "Redis" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 3. " + Colors.FG.LightBlue + "RabbitMQ" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 4. " + Colors.FG.LightBlue + "Varnish" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 5. " + Colors.FG.LightBlue + "Cron" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 6. " + Colors.FG.LightBlue + "Caches/Autoscaling" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 7. " + Colors.FG.LightBlue + "MySQL" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 8. " + Colors.FG.LightBlue + "ElasticSearch" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 9. " + Colors.FG.LightBlue + "Development Copy" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 10. " + Colors.FG.LightBlue + "Exit" + Colors.Reset)
        print(Colors.FG.Green + "+---------=> " + Colors.FG.Yellow + "Version " + version + " " + Colors.FG.Green + "<=---------+" + Colors.Reset)

        choice = input(Colors.FG.Yellow + "Choose Menu Item: " + Colors.Reset)

        if choice == "10":
            sys.exit()
        elif choice == "9":
            dev_copy_menu(config, path)
        elif choice == "8":
            elasticsearch_menu(config, path)
        elif choice == "7":
            mysql_menu(config, path)
        elif choice == "6":
            cache_menu(config, path)
        elif choice == "5":
            cron_menu(config, path)
        elif choice == "4":
            varnish_menu(config, path)
        elif choice == "3":
            rabbit_menu(config, path)
        elif choice == "2":
            redis_menu(config, path)
        elif choice == "1":
            magento_menu(config, path)
        else:
            print(Colors.FG.Red + Colors.Bold + "Invalid menu choice." + Colors.Reset)
            main_menu(path)

def redis_menu(config, path):
    choice = '0'
    while choice == '0':
        print(Colors.FG.Green + "++++++=> " + Colors.FG.LightBlue + "Redis Menu:" + Colors.FG.Green + " <=++++++" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 1. " + Colors.FG.LightBlue + "Configure Redis Sessions" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 2. " + Colors.FG.LightBlue + "Configure Redis Cache" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 3. " + Colors.FG.LightBlue + "Back" + Colors.Reset)
        print(Colors.FG.Green + "+---------=> " + Colors.FG.Yellow + "Version " + version + " " + Colors.FG.Green + "<=---------+" + Colors.Reset)

        choice = input(Colors.FG.Yellow + "Choose Menu Item: " + Colors.Reset)

        if choice == "3":
            main_menu(path)
        elif choice == "2":
            Redis.check_redis_cache(config, path, 1)
        elif choice == "1":
            Redis.check_redis_sessions(config, path, 1)
        else:
            print(Colors.FG.Red + Colors.Bold + "Invalid menu choice." + Colors.Reset)
            redis_menu(config, path)


def rabbit_menu(config, path):
    choice = '0'
    while choice == '0':
        print(Colors.FG.Green + "++++++=> " + Colors.FG.LightBlue + "RabbitmQ Menu:" + Colors.FG.Green + " <=++++++" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 1. " + Colors.FG.LightBlue + "Configure RabbitMQ" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 2. " + Colors.FG.LightBlue + "Back" + Colors.Reset)
        print(Colors.FG.Green + "+---------=> " + Colors.FG.Yellow + "Version " + version + " " + Colors.FG.Green + "<=---------+" + Colors.Reset)

        choice = input(Colors.FG.Yellow + "Choose Menu Item: " + Colors.Reset)

        if choice == "2":
            main_menu(path)
        elif choice == "1":
            Rabbit.check_rabbitmq(config, path, 1)
        else:
            print(Colors.FG.Red + Colors.Bold + "Invalid menu choice." + Colors.Reset)
            rabbit_menu(config, path)

def magento_menu(config, path):
    choice = '0'
    while choice == '0':
        print(Colors.FG.Green + "++++++=> " + Colors.FG.LightBlue + "Magento Menu:" + Colors.FG.Green + " <=++++++" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 1. " + Colors.FG.LightBlue + "Reindex All" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 2. " + Colors.FG.LightBlue + "Reset Indexes" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 3. " + Colors.FG.LightBlue + "Set Indexes to Schedule" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 4. " + Colors.FG.LightBlue + "Magento Database Upgrade" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 5. " + Colors.FG.LightBlue + "Magento Compile" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 6. " + Colors.FG.LightBlue + "Deploy Static Content" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 7. " + Colors.FG.LightBlue + "Patch Magento" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 8. " + Colors.FG.LightBlue + "Magento Backup" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 9. " + Colors.FG.LightBlue + "Back" + Colors.Reset)
        print(Colors.FG.Green + "+---------=> " + Colors.FG.Yellow + "Version " + version + " " + Colors.FG.Green + "<=---------+" + Colors.Reset)

        choice = input(Colors.FG.Yellow + "Choose Menu Item: " + Colors.Reset)

        if choice == "9":
            main_menu(path)
        elif choice == "8":
            magento_backup_menu(config, path)
        elif choice == "7":
            magento_patch_menu(config, path)
        elif choice == "6":
            Magento.static_content_deploy(config, path)
            magento_menu(config, path)
        elif choice == "5":
            Magento.magento_compile(config, path)
            magento_menu(config, path)
        elif choice == "4":
            Magento.magento_setup_upgrade(config, path)
            magento_menu(config, path)
        elif choice == "3":
            Magento.set_index_to_schedule(config, path)
            magento_menu(config, path)
        elif choice == "2":
            Magento.reset_all_index(config, path)
            magento_menu(config, path)
        elif choice == "1":
            Magento.reset_all_index(config, path)
            Magento.reindex_all_index(config, path)
            magento_menu(config, path)
        else:
            print(Colors.FG.Red + Colors.Bold + "Invalid menu choice." + Colors.Reset)
            magento_menu(config, path)

def magento_patch_menu(config, path):
    choice = '0'
    while choice == '0':
        print(Colors.FG.Green + "++++++=> " + Colors.FG.LightBlue + "Patch Menu:" + Colors.FG.Green + " <=++++++" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 1. " + Colors.FG.LightBlue + "Magento Catalog RabbitMQ Patch" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 2. " + Colors.FG.LightBlue + "Magento Framework PDO Adapter MySQL 8.0" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 3. " + Colors.FG.LightBlue + "Back" + Colors.Reset)
        print(Colors.FG.Green + "+---------=> " + Colors.FG.Yellow + "Version " + version + " " + Colors.FG.Green + "<=---------+" + Colors.Reset)

        choice = input(Colors.FG.Yellow + "Choose Menu Item: " + Colors.Reset)

        if choice == "3":
            main_menu(path)
        elif choice == "2":
            Patches.install_pdo_adapter_mysql8(config, path, 1)
        elif choice == "1":
            Patches.install_catalog_rabbitmq(config, path, 1)
        else:
            print(Colors.FG.Red + Colors.Bold + "Invalid menu choice." + Colors.Reset)
            magento_patch_menu(config, path)

def magento_backup_menu(config, path):
    choice = '0'
    while choice == '0':
        print(Colors.FG.Green + "++++++=> " + Colors.FG.LightBlue + "Backup Menu:" + Colors.FG.Green + " <=++++++" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 1. " + Colors.FG.LightBlue + "Backup Magento S3 Bucket" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 2. " + Colors.FG.LightBlue + "Backup Magento /srv/backups" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 3. " + Colors.FG.LightBlue + "Backup Magento /srv/backups (No Media)" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 4. " + Colors.FG.LightBlue + "Backup Magento Custom" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 5. " + Colors.FG.LightBlue + "Backup Magento Custom (No Media)" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 6. " + Colors.FG.LightBlue + "Back" + Colors.Reset)
        print(Colors.FG.Green + "+---------=> " + Colors.FG.Yellow + "Version " + version + " " + Colors.FG.Green + "<=---------+" + Colors.Reset)

        choice = input(Colors.FG.Yellow + "Choose Menu Item: " + Colors.Reset)

        if choice == "6":
            main_menu(path)
        elif choice == "5":
            Backup.backup_local_custom(config, path, 0, 1)
        elif choice == "4":
            Backup.backup_local_custom(config, path, 1, 1)
        elif choice == "3":
            Backup.backup_local_auto(config, path, 0, 1)
        elif choice == "2":
            Backup.backup_local_auto(config, path, 1, 1)
        elif choice == "1":
            Backup.backup_to_s3_bucket(config, path, 1)
        else:
            print(Colors.FG.Red + Colors.Bold + "Invalid menu choice." + Colors.Reset)
            magento_patch_menu(config, path)

def varnish_menu(config, path):
    choice = '0'
    while choice == '0':
        print(Colors.FG.Green + "++++++=> " + Colors.FG.LightBlue + "Varnish Menu:" + Colors.FG.Green + " <=++++++" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 1. " + Colors.FG.LightBlue + "Configure Varnish" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 2. " + Colors.FG.LightBlue + "Purge Varnish" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 3. " + Colors.FG.LightBlue + "Back" + Colors.Reset)
        print(Colors.FG.Green + "+---------=> " + Colors.FG.Yellow + "Version " + version + " " + Colors.FG.Green + "<=---------+" + Colors.Reset)

        choice = input(Colors.FG.Yellow + "Choose Menu Item: " + Colors.Reset)

        if choice == "3":
            main_menu(path)
        elif choice == "2":
            Varnish.purge_varnish(config, path, 1)
        elif choice == "1":
            Varnish.check_varnish(config, path, 1)
        else:
            print(Colors.FG.Red + Colors.Bold + "Invalid menu choice." + Colors.Reset)
            varnish_menu(config, path)


def cron_menu(config, path):
    choice = '0'
    while choice == '0':
        print(Colors.FG.Green + "++++++=> " + Colors.FG.LightBlue + "Cron Menu:" + Colors.FG.Green + " <=++++++" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 1. " + Colors.FG.LightBlue + "Install MageMojo Cron" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 2. " + Colors.FG.LightBlue + "Reset Crons" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 3. " + Colors.FG.LightBlue + "Back" + Colors.Reset)
        print(Colors.FG.Green + "+---------=> " + Colors.FG.Yellow + "Version " + version + " " + Colors.FG.Green + "<=---------+" + Colors.Reset)

        choice = input(Colors.FG.Yellow + "Choose Menu Item: " + Colors.Reset)

        if choice == "3":
            main_menu(path)
        elif choice == "2":
            Cron.reset_crons(config, path, 1)
        elif choice == "1":
            Cron.install_mmcron(config, path, 1)
        else:
            print(Colors.FG.Red + Colors.Bold + "Invalid menu choice." + Colors.Reset)
            cron_menu(config, path)


def cache_menu(config, path):
    choice = '0'
    while choice == '0':
        print(Colors.FG.Green + "++++++=> " + Colors.FG.LightBlue + "Cache Menu:" + Colors.FG.Green + " <=++++++" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 1. " + Colors.FG.LightBlue + "Clear All Cache" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 2. " + Colors.FG.LightBlue + "Clear Magento Cache" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 3. " + Colors.FG.LightBlue + "Clear Redis Cache" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 4. " + Colors.FG.LightBlue + "Clear Cloudfront Cache" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 5. " + Colors.FG.LightBlue + "Autoscaling Reinit" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 6. " + Colors.FG.LightBlue + "Back" + Colors.Reset)
        print(Colors.FG.Green + "+---------=> " + Colors.FG.Yellow + "Version " + version + " " + Colors.FG.Green + "<=---------+" + Colors.Reset)

        choice = input(Colors.FG.Yellow + "Choose Menu Item: " + Colors.Reset)

        if choice == "6":
            main_menu(path)
        elif choice == "5":
            Cache.reinit_as(config, path, 1)
        elif choice == "4":
            Cache.clear_cloudfront(config, path, 1)
        elif choice == "3":
            Cache.clear_redis(config, path, 1)
        elif choice == "2":
            Cache.clear_magento(config, path, 1)
        elif choice == "1":
            Cache.clear_all(config, path, 1)

        else:
            print(Colors.FG.Red + Colors.Bold + "Invalid menu choice." + Colors.Reset)
            redis_menu(config, path)


def mysql_menu(config, path):
    choice = '0'
    while choice == '0':
        print(Colors.FG.Green + "++++++=> " + Colors.FG.LightBlue + "MySQL Menu:" + Colors.FG.Green + " <=++++++" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 1. " + Colors.FG.LightBlue + "Update MySQL Credentials Auto" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 2. " + Colors.FG.LightBlue + "Update MySQL Credentials Manual" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 3. " + Colors.FG.LightBlue + "Backup Database Auto" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 4. " + Colors.FG.LightBlue + "Backup Database Manual" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 5. " + Colors.FG.LightBlue + "Back" + Colors.Reset)
        print(Colors.FG.Green + "+---------=> " + Colors.FG.Yellow + "Version " + version + " " + Colors.FG.Green + "<=---------+" + Colors.Reset)

        choice = input(Colors.FG.Yellow + "Choose Menu Item: " + Colors.Reset)

        if choice == "5":
            main_menu(path)
        elif choice == "4":
            Mysql.mysql_dump_manual(config, path, 1)
        elif choice == "3":
            Mysql.mysql_dump_auto(config, path, "/srv/backups", 1)
        elif choice == "2":
            Mysql.update_mysql_credentials_manual(config, path, 1)
        elif choice == "1":
            Mysql.update_mysql_credentials_from_system(config, path, 1)
        else:
            print(Colors.FG.Red + Colors.Bold + "Invalid menu choice." + Colors.Reset)
            mysql_menu(config, path)

def elasticsearch_menu(config, path):
    choice = '0'
    while choice == '0':
        print(Colors.FG.Green + "++++++=> " + Colors.FG.LightBlue + "Elasticsearch Menu:" + Colors.FG.Green + " <=++++++" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 1. " + Colors.FG.LightBlue + "Configure Elasticsearch" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 2. " + Colors.FG.LightBlue + "Reindex Search Catalog" + Colors.Reset)
        print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 3. " + Colors.FG.LightBlue + "Back" + Colors.Reset)
        print(Colors.FG.Green + "+---------=> " + Colors.FG.Yellow + "Version " + version + " " + Colors.FG.Green + "<=---------+" + Colors.Reset)

        choice = input(Colors.FG.Yellow + "Choose Menu Item: " + Colors.Reset)

        if choice == "3":
            main_menu(path)
        elif choice == "2":
            ElasticSearch.reindex_elasticsearch(config, path, 1)
        elif choice == "1":
            ElasticSearch.configure_elasticsearch(config, path, 1)
        else:
            print(Colors.FG.Red + Colors.Bold + "Invalid menu choice." + Colors.Reset)
            elasticsearch_menu(config, path)

def dev_copy_menu(config, path):
    choice = '0'
    while choice == '0':
        if config is False and path is False:
            print(Colors.FG.Green + "++++++=> " + Colors.FG.LightBlue + "Dev Copy Menu:" + Colors.FG.Green + " <=++++++" + Colors.Reset)
            print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 1. " + Colors.FG.LightBlue + "Dev Copy Default" + Colors.Reset)
            print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 2. " + Colors.FG.LightBlue + "Dev Copy No Media" + Colors.Reset)
            print(Colors.FG.Green + "=>" + Colors.FG.LightGrey + " 3. " + Colors.FG.LightGrey + "Exit" + Colors.Reset)
            print(Colors.FG.Green + "+---------=> " + Colors.FG.Yellow + "Version " + version + " " + Colors.FG.Green + "<=---------+" + Colors.Reset)

            choice = input(Colors.FG.Yellow + "Choose Menu Item: " + Colors.Reset)
            if choice == "3":
                sys.exit()
            elif choice == "2":
                dev_copy_menu(config, path)
            elif choice == "1":
                Dev.dev_copy_default(config, path, 1)
            else:
                print(Colors.FG.Red + Colors.Bold + "Invalid menu choice." + Colors.Reset)
                dev_copy_menu(config, path)
        else:
            print(Colors.FG.Green + "++++++=> " + Colors.FG.LightBlue + "Dev Copy Menu:" + Colors.FG.Green + " <=++++++" + Colors.Reset)
            print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 1. " + Colors.FG.LightBlue + "Dev Copy Default" + Colors.Reset)
            print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 2. " + Colors.FG.LightBlue + "Dev Copy No Media" + Colors.Reset)
            print(Colors.FG.Green + "=>" + Colors.FG.Yellow + " 3. " + Colors.FG.LightBlue + "Back" + Colors.Reset)
            print(Colors.FG.Green + "+---------=> " + Colors.FG.Yellow + "Version " + version + " " + Colors.FG.Green + "<=---------+" + Colors.Reset)

            choice = input(Colors.FG.Yellow + "Choose Menu Item: " + Colors.Reset)
            if choice == "3":
                main_menu(config)
            elif choice == "2":
                dev_copy_menu(config, path)
            elif choice == "1":
                Dev.dev_copy_default(config, path, 1)
            else:
                print(Colors.FG.Red + Colors.Bold + "Invalid menu choice." + Colors.Reset)
                main_menu(config)