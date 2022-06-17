import lib.menu_handler as menu
import lib.config_handler as conf


def main():
    path = conf.get_path()
    menu.main_menu(path)


main()
