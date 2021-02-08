import lib.menu_handler as Menu
import lib.config_handler as conf
from lib.text_color import Colors

def main():
   path = conf.get_path()
   config = conf.load_config(path)
   Menu.main_menu(config, path)

main()
