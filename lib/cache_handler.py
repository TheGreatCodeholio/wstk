import lib.menu_handler as menu
import lib.command_handler as shell
from lib.text_color import Colors


def clear_magento(config, path, menu_return):
    action = "Clear Magento Cache"
    print(Colors.FG.LightGreen + "Clearing Magento Cache" + Colors.Reset)
    shell.run_bash_command(config, path, action, "php -ddisplay_errors=on " + path + "/bin/magento cache:flush", "Magento Cache Flush Complete")
    shell.run_bash_command(config, path, action, "php -ddisplay_errors=on " + path + "/bin/magento cache:clean", "Magento Cache Clean Complete")
    if menu_return == 1:
        menu.cache_menu(config, path)


def clear_redis(config, path, menu_return):
    action = "Clear Redis Cache"
    print(Colors.FG.LightGreen + "Clearing Redis Cache" + Colors.Reset)
    shell.run_bash_command(config, path, action, "redis-cli -h redis flushall", "Cleared Redis Cache")
    if menu_return == 1:
        menu.cache_menu(config, path)


def clear_cloudfront(config, path, menu_return):
    action = "Clear CloudFront Cache"
    print(Colors.FG.LightGreen + "Clearing CloudFront Cache" + Colors.Reset)
    shell.run_bash_command(config, path, action, "/usr/share/stratus/cli cache.all.clear", "Cleared CloudFront Cache")
    if menu_return == 1:
        menu.cache_menu(config, path)


def reinit_as(config, path, menu_return):
    action = "Reinitialize Autoscaling"
    print(Colors.FG.LightGreen + "Reinitializing Autoscaling" + Colors.Reset)
    shell.run_bash_command(config, path, action, "/usr/share/stratus/cli zerodowntime.init", "New Autoscale Pods Deployed")
    shell.run_bash_command(config, path, action, "/usr/share/stratus/cli zerodowntime.switch", "Autoscaling Pods Switched")
    if menu_return == 1:
        menu.cache_menu(config, path)


def clear_all(config, path, menu_return):
    action = "Clear All Caches"
    print(Colors.FG.LightGreen + "Clearing All Caches" + Colors.Reset)
    shell.run_bash_command(config, path, action, "php -ddisplay_errors=on " + path + "/bin/magento cache:flush", "Magento Cache Flush Complete")
    shell.run_bash_command(config, path, action, "php -ddisplay_errors=on " + path + "/bin/magento cache:clean", "Magento Cache Clean Complete")
    shell.run_bash_command(config, path, action, "redis-cli -h redis flushall", "Cleared Redis Cache")
    shell.run_bash_command(config, path, action, "/usr/share/stratus/cli cache.all.clear", "Cleared CloudFront Cache")
    if menu_return == 1:
        menu.cache_menu(config, path)


def clear_all_reinit(config, path, menu_return):
    action = "Clear All Caches and Reinitialize Autoscaling"
    print(Colors.FG.LightGreen + "Clearing All Caches and Reinitializing Autoscaling" + Colors.Reset)
    shell.run_bash_command(config, path, action, "php -ddisplay_errors=on " + path + "/bin/magento cache:flush", "Magento Cache Flush Complete")
    shell.run_bash_command(config, path, action, "php -ddisplay_errors=on " + path + "/bin/magento cache:clean", "Magento Cache Clean Complete")
    shell.run_bash_command(config, path, action, "redis-cli -h redis flushall", "Cleared Redis Cache")
    shell.run_bash_command(config, path, action, "/usr/share/stratus/cli cache.all.clear", "Cleared CloudFront Cache")
    shell.run_bash_command(config, path, action, "/usr/share/stratus/cli zerodowntime.init", "New Autoscale Pods Deployed")
    shell.run_bash_command(config, path, action, "/usr/share/stratus/cli zerodowntime.switch", "Autoscaling Pods Switched")
    if menu_return == 1:
        menu.cache_menu(config, path)
