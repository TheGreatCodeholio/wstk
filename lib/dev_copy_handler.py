import datetime
import json
import re
import subprocess
import time

import lib.menu_handler as menu
import lib.mysql_handler as Mysql
import lib.magento_handler as Mage
import lib.cache_handler as cache
from lib.text_color import Colors
import lib.command_handler as shell
import lib.magento_handler as mage
import os


def dev_copy_default(config, path, media):
    action = "Development Copy"
    # Get User Input
    user_input = UserInput()
    # Put Data in to Dict
    settings_dict = user_input.settings_dict
    settings_dict["prod_ssh_privkey_path"] = check_for_ssh_key(settings_dict["prod_ssh_user"])
    pub_key = os.popen("cat /srv/.ssh/" + settings_dict["prod_ssh_user"] + ".pub").read()
    print(Colors.FG.Yellow + "Add SSH Key to Production Stratus User: " + Colors.Reset + Colors.FG.LightGreen +
          settings_dict[
              "prod_ssh_user"] + Colors.Reset)
    print(Colors.FG.LightBlue + pub_key + Colors.Reset)
    dev_ip = os.popen("curl http://ipcheck.com/").read()
    print(Colors.FG.Yellow + "Add SSH User " + Colors.Reset + Colors.FG.LightGreen + settings_dict[
        "prod_ssh_user"] + Colors.Reset + Colors.FG.Yellow + " to Production whitelist and add IP address: " + Colors.Reset + Colors.FG.LightGreen + dev_ip + Colors.Reset)
    input(Colors.FG.Yellow + "Press Any Key to continue..." + Colors.Reset)
    # Backup Source Database
    print(Colors.FG.LightGreen + Colors.Bold + "Starting Production Database Backup" + Colors.Reset)
    time.sleep(1.5)
    backup_source_database(settings_dict)
    print(Colors.FG.LightGreen + Colors.Bold + "Starting Database Import From Production" + Colors.Reset)
    time.sleep(1.5)
    import_source_database(settings_dict)
    print(Colors.FG.LightGreen + Colors.Bold + "Starting RSYNC Files From Production" + Colors.Reset)
    time.sleep(1.5)
    rsync_production_files(settings_dict)
    print(Colors.FG.LightGreen + Colors.Bold + "Doing Dev Copy Configuration for Magento 2" + Colors.Reset)
    time.sleep(1.5)
    dev_config(settings_dict, config).init_config()
    Mage.reindex_all_index(config, settings_dict["prod_public_html"])
    Mage.magento_compile(config, settings_dict["prod_public_html"])
    Mage.static_content_deploy(config, settings_dict["prod_public_html"])
    cache.clear_all_reinit(config, settings_dict["prod_public_html"])
    print(Colors.FG.LightGreen + action + " Complete!" + Colors.Reset)


def check_for_ssh_key(ssh_user):
    if os.path.exists("/srv/.ssh/" + ssh_user):
        print(Colors.FG.LightBlue + "Key Exists for " + Colors.Reset + Colors.FG.LightGreen + ssh_user + Colors.Reset)
        return "/srv/.ssh/" + ssh_user
    else:
        print(Colors.FG.LightGreen + "Creating Key for " + Colors.Reset + Colors.FG.LightBlue + ssh_user + Colors.Reset)
        os.popen("ssh-keygen -t rsa -N \"\" -f ~/.ssh/" + ssh_user).read()
        return "/srv/.ssh/" + ssh_user


def backup_source_database(settings_dict):
    # Get Remote Database Credentials via SSH
    print(Colors.FG.LightGreen + Colors.Bold + "Getting Production Database Credentials." + Colors.Reset)
    dump_creds = os.popen(
        "ssh -i " + settings_dict["prod_ssh_privkey_path"] + " " + settings_dict["prod_ssh_user"] + "@" + settings_dict[
            "prod_ssh_host"] + " -p" + settings_dict[
            "prod_ssh_port"] + " '/usr/share/stratus/cli database.config > cred.log 2>&1; cat cred.log'").read()
    os.popen(
        "ssh -i " + settings_dict["prod_ssh_privkey_path"] + " " + settings_dict["prod_ssh_user"] + "@" + settings_dict[
            "prod_ssh_host"] + " -p" + settings_dict["prod_ssh_port"] + " 'rm cred.log'")
    cred_file = open("remote_creds.log", "w")
    cred_file.write(dump_creds)
    cred_file.close()
    # Read Credentials to our settings Dictionary
    settings_dict["prod_mysql_user"] = \
        os.popen(
            "cat remote_creds.log | grep Username | awk '{print $3}' | cut -c3- | rev | cut -c4- | rev").read().split(
            '\n')[0]
    settings_dict["prod_mysql_database"] = \
        os.popen(
            "cat remote_creds.log | grep Username | awk '{print $7}' | cut -c3- | rev | cut -c4- | rev").read().split(
            '\n')[0]
    settings_dict["prod_mysql_password"] = \
        os.popen(
            "cat remote_creds.log | grep Username | awk '{print $14}' | cut -c3- | rev | cut -c4- | rev").read().split(
            '\n')[0]
    os.popen("rm remote_creds.log")
    # MySQL Dump Database
    print(Colors.FG.LightGreen + Colors.Bold + "Dumping Production Database." + Colors.Reset)
    os.popen(
        "ssh -i " + settings_dict["prod_ssh_privkey_path"] + " " + settings_dict["prod_ssh_user"] + "@" + settings_dict[
            "prod_ssh_host"] + " -p" + settings_dict[
            "prod_ssh_port"] + " 'mysqldump --skip-lock-tables --extended-insert=FALSE --verbose -h mysql --quick -u " +
        settings_dict["prod_mysql_user"] + " -p" + settings_dict["prod_mysql_password"] + " " + settings_dict[
            "prod_mysql_database"] + " > /srv/db_" + settings_dict["date"] + ".sql'").read()
    # Check if backups directory exists locally
    if not os.path.exists("/srv/backups"):
        os.popen("mkdir /srv/backups")
    # RSYNC Database Dump to Local backups folder.
    print(Colors.FG.LightGreen + Colors.Bold + "RSYNC Production Database to Dev." + Colors.Reset)
    os.popen("rsync -Pav -e 'ssh -p " + settings_dict["prod_ssh_port"] + " -i " + settings_dict[
        "prod_ssh_privkey_path"] + "' " + settings_dict["prod_ssh_user"] + "@" + settings_dict[
                 "prod_ssh_host"] + ":/srv/db_" + settings_dict["date"] + ".sql /srv/backups/").read()
    # Finished with database backup.


def import_source_database(settings_dict):
    # Check for old database, remove if it exists.
    if os.path.exists("/srv/backups/fixed_dump.sql"):
        os.popen("rm /srv/backups/fixed_dump.sql")
    # Fix SUPER Privs
    print(Colors.FG.LightGreen + Colors.Bold + "Fixing Super Privileges." + Colors.Reset)
    os.popen("sed -E 's/DEFINER=`[^`]+`@`[^`]+`/DEFINER=CURRENT_USER/g' /srv/backups/db_" + settings_dict[
        "date"] + ".sql > /srv/backups/fixed_dump.sql")
    # Drop Old Database
    os.popen("mysql -h mysql -u " + settings_dict["dev_mysql_user"] + " -p'" + settings_dict[
        "dev_mysql_password"] + "' -e 'drop database " + settings_dict["dev_mysql_database"] + "'").read()
    # Create Blank Database
    os.popen("mysql -h mysql -u " + settings_dict["dev_mysql_user"] + " -p'" + settings_dict[
        "dev_mysql_password"] + "' -e 'create database " + settings_dict["dev_mysql_database"] + "'").read()
    # Import Fixed Dump
    print(Colors.FG.LightGreen + Colors.Bold + "Importing Production Database to Dev." + Colors.Reset)
    os.popen(
        "mysql -h mysql -u " + settings_dict["dev_mysql_user"] + " -p'" + settings_dict["dev_mysql_password"] + "' " +
        settings_dict["dev_mysql_database"] + " < /srv/backups/fixed_dump.sql").read()
    # Remove fixed database, keeping synced one for backup.
    os.popen("rm /srv/backups/fixed_dump.sql")
    # Finished Import


def rsync_production_files(settings_dict):
    if os.path.exists(settings_dict["prod_public_html"]):
        child = subprocess.Popen("rm -rf " + settings_dict["prod_public_html"], shell=True, stdout=subprocess.PIPE)
        streamdata = child.communicate()[0]
        rc = child.returncode
    print(Colors.FG.LightGreen + Colors.Bold + "RSYNC Prod Files to Dev." + Colors.Reset)
    os.popen("rsync -Pav -e 'ssh -p " + settings_dict["prod_ssh_port"] + " -i " + settings_dict[
        "prod_ssh_privkey_path"] + "' " + settings_dict["prod_ssh_user"] + "@" + settings_dict["prod_ssh_host"] + ":" +
             settings_dict["prod_public_html"] + " /srv/").read()


class UserInput:
    def __init__(self):
        self.settings_dict = {}
        self.today = datetime.datetime.now()
        self.settings_dict["current_date"] = self.today.strftime("%d%B%Y")
        self.get_uuid()

    def get_uuid(self):
        dev_uuid = input(Colors.FG.Yellow + "Dev Instance UUID: " + Colors.Reset)
        if len(dev_uuid) != 16:
            print(Colors.BG.Red + Colors.Bold + "UUID must be exactly 16 Characters." + Colors.Reset)
            self.get_uuid()
            return
        self.settings_dict["dev_uuid"] = dev_uuid
        self.check_for_config()

    def check_for_config(self):
        if os.path.exists("var/instance_configs/" + self.settings_dict["dev_uuid"] + ".json"):
            print(Colors.FG.LightGreen + Colors.Bold + "Existing Config Found!" + Colors.Reset)
            config_load = input(Colors.FG.Yellow + "Would you like to load existing config? (y/n): " + Colors.Reset)
            if config_load.lower() == "y" or config_load.lower() == "yes":
                print(Colors.FG.LightGreen + Colors.Bold + "Loading Existing Config..." + Colors.Reset)
                with open("var/instance_configs/" + self.settings_dict["dev_uuid"] + ".json", 'r') as config_json:
                    self.settings_dict = json.load(config_json)
                    config_json.close()
            elif config_load.lower() == "n" or config_load.lower() == "no":
                print(Colors.FG.LightBlue + "Not Loading Existing Config..." + Colors.Reset)
                self.get_dev_mysql_cred()
            else:
                print(Colors.BG.Red + "Answer with the following, Yes/Y or No/N" + Colors.Reset)
                self.check_for_config()
                return
        else:
            print(Colors.BG.Orange + "Existing Config Not Found!" + Colors.Reset)
            self.get_dev_mysql_cred()

    def get_dev_mysql_cred(self):
        db_creds = Mysql.get_mysql_credentials()
        if db_creds:
            self.settings_dict["dev_mysql_user"] = db_creds["Username"]
            self.settings_dict["dev_mysql_database"] = db_creds["Name"]
            self.settings_dict["dev_mysql_password"] = db_creds["Password"]
        else:
            print(Colors.BG.Red + "Could not get Dev Database Credentials." + Colors.Reset)
            db_creds = {}
            db_creds["Name"] = input(Colors.FG.Yellow + "Dev MySQL Database Name: " + Colors.Reset)
            db_creds["Username"] = input(Colors.FG.Yellow + "Dev MySQL Username: " + Colors.Reset)
            db_creds["Password"] = input(Colors.FG.Yellow + "Dev MySQL Password: " + Colors.Reset)
            # TODO Sanitize Input
            self.settings_dict["dev_mysql_user"] = db_creds["Username"]
            self.settings_dict["dev_mysql_database"] = db_creds["Name"]
            self.settings_dict["dev_mysql_password"] = db_creds["Password"]

        self.get_dev_baseurl()

    def get_dev_baseurl(self):
        child = subprocess.Popen(
            "mysql -h mysql -u " + self.settings_dict["dev_mysql_user"] + " -p'" + self.settings_dict[
                "dev_mysql_password"] + "' " + self.settings_dict[
                "dev_mysql_database"] + " -e 'select value from core_config_data where path like \"web/%secure/base_url\" AND scope=\"default\" LIMIT 1'",
            shell=True, stdout=subprocess.PIPE)
        streamdata = child.communicate()[0]
        rc = child.returncode
        if rc == 1:
            base_url = input(Colors.FG.Yellow + "Target Base URL: " + Colors.Reset)
            if not base_url.endswith('/'):
                print(Colors.BG.Red + "Base URL must end with a /." + Colors.Reset)
                self.get_dev_baseurl()
                return
            else:
                self.settings_dict["dev_base_url"] = base_url
        else:
            self.settings_dict["dev_base_url"] = streamdata.decode('UTF-8').split('value')[1].replace('\n', '')
        self.get_prod_ssh_host()

    def get_prod_ssh_host(self):
        prod_ssh_host = input(Colors.FG.Yellow + "Production SSH Host IP: " + Colors.Reset)
        try:
            ip_valid = [0 <= int(x) < 256 for x in
                        re.split('\.', re.match(r'^\d+\.\d+\.\d+\.\d+$', prod_ssh_host).group(0))].count(True) == 4
            if not ip_valid:
                raise ValueError
            else:
                self.settings_dict["prod_ssh_host"] = prod_ssh_host
                self.get_prod_ssh_port()
        except ValueError:
            print(Colors.BG.Red + "Not a Valid IPv4 Address." + Colors.Reset)
            self.get_prod_ssh_host()
            return

    def get_prod_ssh_port(self):
        prod_ssh_port = input(Colors.FG.Yellow + "Production SSH Port: " + Colors.Reset)
        self.settings_dict["prod_ssh_port"] = prod_ssh_port
        self.get_prod_ssh_user()

    def get_prod_ssh_user(self):
        prod_ssh_user = input(Colors.FG.Yellow + "Production SSH User: " + Colors.Reset)
        self.settings_dict["prod_ssh_user"] = prod_ssh_user
        self.get_prod_public_html()

    def get_prod_public_html(self):
        prod_public_html = input(Colors.FG.Yellow + "Production public_html path: " + Colors.Reset)
        if prod_public_html.endswith('/'):
            path_length = len(prod_public_html)
            self.settings_dict["prod_public_html"] = prod_public_html[:path_length - 1]
        else:
            self.settings_dict["prod_public_html"] = prod_public_html

        self.save_instance_config()

    def save_instance_config(self):
        print(Colors.FG.LightGreen + Colors.Bold + "Saving Config....." + Colors.Reset)
        with open("var/instance_configs/" + self.settings_dict["dev_uuid"] + ".json", 'w') as outfile:
            json.dump(self.settings_dict, outfile, indent=4)
            outfile.close()


class dev_config:
    def __init__(self, settings_dict, config):
        self.settings_dict = settings_dict
        self.m2_config_json = {}
        self.config = config
        self.init_config()

    def init_config(self):
        if not os.path.exists(self.settings_dict["prod_public_html"] + "/app/etc/env.php"):
            print(Colors.BG.Red + "Magento 2 Configuration doesn't exist, exiting" + Colors.Reset)
            exit(1)
        load_config = subprocess.check_output(
            ["php", "-r",
             "echo json_encode(include '" + self.settings_dict["prod_public_html"] + "/app/etc/env.php');"])
        self.m2_config_json = json.loads(load_config)
        self.config_database()

    def config_database(self):
        print(Colors.FG.LightGreen + Colors.Bold + "Configuring Database." + Colors.Reset)
        Mysql.update_mysql_credentials_from_system(self.config, self.settings_dict["prod_public_html"])
        self.config_downloadable_domains()

    def config_downloadable_domains(self):
        print(Colors.FG.LightGreen + Colors.Bold + "Configuring Downloadable Domains." + Colors.Reset)
        os.popen("php " + self.settings_dict["prod_public_html"] + "/bin/magento downloadable:domains:add " +
                 self.settings_dict["dev_base_url"].split('https://')[1].split('/')[0]).read()
        self.update_base_url()

    def update_base_url(self):
        print(Colors.FG.LightGreen + Colors.Bold + "Updating Base URL" + Colors.Reset)
        os.popen("mysql -h mysql -u " + self.settings_dict["dev_mysql_user"] + " -p\"" + self.settings_dict[
            "dev_mysql_password"] + "\" " + self.settings_dict["dev_mysql_database"] + " -e 'update " +
                 self.m2_config_json["db"]["table_prefix"] + "core_config_data set value=\"" + self.settings_dict[
                     "dev_base_url"] + "\" where path like \"web/%secure/base_url\" AND scope=\"default\"'").read()
        self.update_cookie_domain()

    def update_cookie_domain(self):
        print(Colors.FG.LightGreen + Colors.Bold + "Updating Cookie Domain" + Colors.Reset)
        os.popen("mysql -h mysql -u " + self.settings_dict["dev_mysql_user"] + " -p\"" + self.settings_dict[
            "dev_mysql_password"] + "\" " + self.settings_dict["dev_mysql_database"] + " -e 'update " +
                 self.m2_config_json["db"]["table_prefix"] + "core_config_data set value=\"" +
                 self.settings_dict["dev_base_url"].split('https://')[1].split('/')[
                     0] + "\" where path like \"%cookie_domain%\" AND scope_id=\"0\"'").read()
