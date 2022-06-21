import datetime
import json
import re
import subprocess
import sys
import time

import lib.menu_handler as menu
import lib.mysql_handler as Mysql
import lib.magento_handler as Mage
import lib.cache_handler as cache
from lib.text_color import Colors
import lib.command_handler as shell
import lib.rabbitmq_handler as Rabbit
import lib.config_handler as conf
import os


def dev_copy_default(config, path, media):
    action = "Development Copy"
    # Get User Input
    user_input = UserInput()
    # Put Data in to Dict
    settings_dict = user_input.settings_dict
    # Backup Source Database
    print(Colors.FG.LightGreen + Colors.Bold + "Starting Production Database Backup" + Colors.Reset)
    time.sleep(1.5)
    Mysql.backup_remote_database(settings_dict)
    print(Colors.FG.LightGreen + Colors.Bold + "Starting Database Import From Production" + Colors.Reset)
    time.sleep(1.5)
    Mysql.import_remote_database(settings_dict)
    time.sleep(1.5)
    rsync_production_files(settings_dict)
    print(Colors.FG.LightGreen + Colors.Bold + "Doing Dev Copy Configuration for Magento 2" + Colors.Reset)
    time.sleep(1.5)
    config = conf.load_config(settings_dict["prod_public_html"])
    dev_config(settings_dict, config).init_config()
    config = conf.load_config(settings_dict["prod_public_html"])
    if "queue" in config:
        if "amqp" in config["queue"]:
            Rabbit.check_rabbitmq(config, settings_dict["prod_public_html"], 0)
    Mage.reindex_all_index(config, settings_dict["prod_public_html"])
    Mage.magento_compile(config, settings_dict["prod_public_html"])
    Mage.static_content_deploy(config, settings_dict["prod_public_html"])
    cache.clear_all_reinit(config, settings_dict["prod_public_html"], 0)
    print(Colors.FG.LightGreen + action + " Complete!" + Colors.Reset)
    menu.main_menu(settings_dict["prod_public_html"])


def check_for_ssh_key(ssh_user):
    if os.path.exists("/srv/.ssh/" + ssh_user):
        print(Colors.FG.LightBlue + "Key Exists for " + Colors.Reset + Colors.FG.LightGreen + ssh_user + Colors.Reset)
        return "/srv/.ssh/" + ssh_user
    else:
        print(Colors.FG.LightGreen + "Creating Key for " + Colors.Reset + Colors.FG.LightBlue + ssh_user + Colors.Reset)
        os.popen("ssh-keygen -t rsa -N \"\" -f ~/.ssh/" + ssh_user).read()
        return "/srv/.ssh/" + ssh_user


def rsync_production_files(settings_dict):
    action = "RSYNC Prod Files to Dev."

    # remove the root path on dev instance
    if os.path.exists(settings_dict["prod_public_html"]):
        shell.run_bash_command_popen(False, False, action, "rm -rf " + settings_dict["prod_public_html"], "")

    print(Colors.FG.LightGreen + Colors.Bold + "Starting " + action + Colors.Reset)
    if settings_dict["root_is_symlink"] is True:
        # remove last portion of link path for rsync target
        new = settings_dict["root_symlink"]["link_path"].split("/")
        for l in new:
            if l == "":
                new.remove(l)
        new_path = "/"
        list_length = len(new) - 1
        for l in range(list_length):
            new_path += new[l] + "/"

        if not os.path.exists(new_path):
            child = subprocess.Popen("mkdir -p " + new_path, shell=True, stdout=subprocess.PIPE)
            streamdata = child.communicate()[0]
            rc = child.returncode

        # rsync link path to dev from production
        shell.run_bash_command_popen(False, False, action,
                                     "rsync -Pavl -e 'ssh -p " + settings_dict["prod_ssh_port"] + " -i " +
                                     settings_dict[
                                         "prod_ssh_privkey_path"] + "' " + settings_dict["prod_ssh_user"] + "@" +
                                     settings_dict["prod_ssh_host"] + ":" +
                                     settings_dict["root_symlink"]["link_path"] + " " + new_path, ".")
        # recreate symlink
        shell.run_bash_command(False, False, action,
            "ssh -i " + settings_dict["prod_ssh_privkey_path"] + " " + settings_dict[
                "prod_ssh_user"] + "@" + settings_dict["prod_ssh_host"] + " -p" + settings_dict[
                "prod_ssh_port"] + " 'ln -s " + settings_dict["root_symlink"]["link_path"] + " " + settings_dict[
                "prod_public_html"], "..")
    else:
        # remove last portion of root path for rsync target
        new = settings_dict["prod_public_html"].split("/")
        for l in new:
            if l == "":
                new.remove(l)
        new_path = "/"
        list_length = len(new) - 1
        for l in range(list_length):
            new_path += new[l] + "/"

        if not os.path.exists(new_path):
            child = subprocess.Popen("mkdir -p " + new_path, shell=True, stdout=subprocess.PIPE)
            streamdata = child.communicate()[0]
            rc = child.returncode

        # rsync root from production to dev using rsync target
        shell.run_bash_command_popen(False, False, action, "rsync -Pavl -e 'ssh -p " + settings_dict["prod_ssh_port"] + " -i " + settings_dict[
            "prod_ssh_privkey_path"] + "' " + settings_dict["prod_ssh_user"] + "@" + settings_dict["prod_ssh_host"] + ":" +
                 settings_dict["prod_public_html"] + " " + new_path, ".")
        # print second set of . to keep visual progress.
        print(Colors.FG.LightGreen + Colors.Bold + ".." + Colors.Reset)

    # check if we have folder inside root that are symlinks
    if settings_dict["symlink_folders"] is not False:
        count = 3
        folder_list = list(settings_dict["symlink_folders"])
        for f in folder_list:
            # remove folder on dev if exists
            if os.path.exists(f):
                shell.run_bash_command_popen(False, False, action, "rm -rf " + f, "")
            # remove last folder of path ex "/srv/public_html/var" to "/srv/public_html"
            new = f.split("/")
            for l in new:
                if l == "":
                    new.remove(l)
            new_path = "/"
            list_length = len(new) - 1
            for p in range(list_length):
                new_path += new[p] + "/"

            success_message = "." * count
            # create directory if it doesn't exist
            if not os.path.exists(new_path):
                shell.run_bash_command_popen(False, False, action, "mkdir -p " + new_path, success_message)
            count += 1
            success_message = "." * count
            shell.run_bash_command_popen(False, False, action,
                                         "rsync -Pavl -e 'ssh -p " + settings_dict["prod_ssh_port"] + " -i " +
                                         settings_dict[
                                             "prod_ssh_privkey_path"] + "' " + settings_dict["prod_ssh_user"] + "@" +
                                         settings_dict["prod_ssh_host"] + ":" +
                                         f + " " + new_path,
                                         success_message)
            count += 1
    print(Colors.FG.LightGreen + Colors.Bold + action + " Complete!" + Colors.Reset)


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
        self.get_prod_magento_root()

    def get_prod_magento_root(self):
        prod_public_html = input(Colors.FG.Yellow + "Production Magento Root path: " + Colors.Reset)
        if prod_public_html.endswith('/'):
            path_length = len(prod_public_html)
            self.settings_dict["prod_public_html"] = prod_public_html[:path_length - 1]
        elif prod_public_html == "":
            print(Colors.BG.Red + "Must enter a path.." + Colors.Reset)
            self.get_prod_magento_root()
        else:
            self.settings_dict["prod_public_html"] = prod_public_html

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
        self.settings_dict["prod_ssh_privkey_path"] = check_for_ssh_key(self.settings_dict["prod_ssh_user"])
        pub_key = os.popen("cat /srv/.ssh/" + self.settings_dict["prod_ssh_user"] + ".pub").read()
        print(Colors.FG.Yellow + "Add SSH Key to Production Stratus User: " + Colors.Reset + Colors.FG.LightGreen +
              self.settings_dict["prod_ssh_user"] + Colors.Reset)
        print(Colors.FG.LightBlue + pub_key + Colors.Reset)
        dev_ip = os.popen("curl http://ipcheck.com/").read()
        print(Colors.FG.Yellow + "Add SSH User " + Colors.Reset + Colors.FG.LightGreen + self.settings_dict[
            "prod_ssh_user"] + Colors.Reset + Colors.FG.Yellow + " to Production whitelist and add IP address: " + Colors.Reset + Colors.FG.LightGreen + dev_ip + Colors.Reset)
        input(Colors.FG.Yellow + "Press Any Key to continue..." + Colors.Reset)
        self.check_if_root_is_symlink()

    def check_if_root_is_symlink(self):
        check_root_symlink = os.popen(
            "ssh -i " + self.settings_dict["prod_ssh_privkey_path"] + " " + self.settings_dict[
                "prod_ssh_user"] + "@" + self.settings_dict["prod_ssh_host"] + " -p" + self.settings_dict[
                "prod_ssh_port"] + " 'stat " + self.settings_dict[
                "prod_public_html"] + " | head -n1 > sym_check.log; cat sym_check.log'").read()
        os.popen("ssh -i " + self.settings_dict["prod_ssh_privkey_path"] + " " + self.settings_dict[
            "prod_ssh_user"] + "@" + self.settings_dict["prod_ssh_host"] + " -p" + self.settings_dict[
                     "prod_ssh_port"] + " 'rm sym_check.log'")
        cred_file = open("sym_remote_check.log", "w")
        cred_file.write(check_root_symlink)
        cred_file.close()
        is_symlink = os.popen("cat sym_remote_check.log | awk '{print $3}'").read()
        if is_symlink == "->\n":
            self.settings_dict["root_is_symlink"] = True
            new = self.settings_dict["prod_public_html"].split("/")
            for l in new:
                if l == "":
                    new.remove(l)
            new_path = "/"
            list_length = len(new) - 1
            for l in range(list_length):
                new_path += new[l] + "/"

            dump_root_symlink = os.popen(
                "ssh -i " + self.settings_dict["prod_ssh_privkey_path"] + " " + self.settings_dict[
                    "prod_ssh_user"] + "@" + self.settings_dict["prod_ssh_host"] + " -p" + self.settings_dict[
                    "prod_ssh_port"] + " 'find " + new_path + " -type l -ls > root_link.log; cat root_link.log'").read()
            os.popen("ssh -i " + self.settings_dict["prod_ssh_privkey_path"] + " " + self.settings_dict[
                "prod_ssh_user"] + "@" + self.settings_dict["prod_ssh_host"] + " -p" + self.settings_dict[
                         "prod_ssh_port"] + " 'rm root_link.log'")
            cred_file = open("remote_root_link.log", "w")
            cred_file.write(dump_root_symlink)
            cred_file.close()
            symlinks_found = os.popen("cat remote_root_link.log | awk '{print $11, $13}'").read()
            folders = symlinks_found.split("\n")
            for f in folders:
                if f == "":
                    continue
                if f.startswith("."):
                    continue
                full_folder_path = f.split()[0]
                full_link_path = f.split()[1]
                if full_folder_path.startswith("/"):
                    if full_folder_path == self.settings_dict["prod_public_html"]:
                        self.settings_dict["root_symlink"] = {"folder_path": full_folder_path,
                                                              "link_path": full_link_path}
            self.get_prod_symlinks_inside_root_magento()
        else:
            self.settings_dict["root_is_symlink"] = False
            self.get_prod_symlinks_inside_root_magento()

    def get_prod_symlinks_inside_root_magento(self):
        dump_symlinks = os.popen(
            "ssh -i " + self.settings_dict["prod_ssh_privkey_path"] + " " + self.settings_dict["prod_ssh_user"] + "@" +
            self.settings_dict["prod_ssh_host"] + " -p" + self.settings_dict[
                "prod_ssh_port"] + " 'find " + self.settings_dict["prod_public_html"] + "\ -type l -ls > link.txt 2>&1; cat link.txt'").read()
        os.popen("ssh -i " + self.settings_dict["prod_ssh_privkey_path"] + " " + self.settings_dict["prod_ssh_user"] + "@" +
                 self.settings_dict["prod_ssh_host"] + " -p" + self.settings_dict["prod_ssh_port"] + " 'rm link.txt'")
        cred_file = open("remote_links.log", "w")
        cred_file.write(dump_symlinks)
        cred_file.close()
        symlinks = os.popen("cat remote_links.log | awk '{print $13}'").read()
        folders = symlinks.split("\n")
        folder_list = []
        for f in folders:
            if f.startswith("/"):
                if f.endswith("/"):
                    folder_list.append(f[:-1].replace(" ", ""))
                else:
                    folder_list.append(f.replace(" ", ""))
        if len(folder_list) < 1:
            self.settings_dict["symlink_folders"] = False
        else:
            self.settings_dict["symlink_folders"] = folder_list
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
        Mysql.update_mysql_credentials_from_system(self.config, self.settings_dict["prod_public_html"], 0)
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
