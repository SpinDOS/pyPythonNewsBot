import sys
import time
from python_news_db_manager import PythonNewsDbManager
from python_news_update_manager import PythonNewsUpdateManager
from habrahabr_news_loader import HabraHabrNewsLoader
from linux_org_news_loader import LinuxOrgNewsLoader
from tproger_news_loader import TProgerNewsLoader
from vk_news_loader import VkNewsLoader


class ConsoleLogger(object):
    @staticmethod
    def log_message(message):
        print(message)


def configure_update_manager(db_manager, logger=ConsoleLogger()):
    manager = PythonNewsUpdateManager(db_manager, logger)
    manager.add_news_loader(HabraHabrNewsLoader())
    manager.add_news_loader(LinuxOrgNewsLoader())
    manager.add_news_loader(TProgerNewsLoader())
    manager.add_news_loader(VkNewsLoader())
    return manager


def _print_help():
    print("Usage: python python_news_updater.py [db_filename] [--auto]")
    print("-auto parameter makes program to stay "
          "in memory and update news every 3 hours")
    print("Environment variable VK_API_KEY allow you "
          "to specify access token for vk.com (https://vk.com/dev/access_token)")


def update_news_with_console_output(auto_mode, db_filename):
    news_manager = configure_update_manager(PythonNewsDbManager(db_filename))
    if not auto_mode:
        news_manager.update_news_in_db()
        print("Done!")
        return

    print("News manager will update news every 3 hours. Press Ctrl+C to exit")
    three_hours_in_seconds = 3 * 60 * 60
    while True:
        news_manager.update_news_in_db()
        print(time.strftime("%H:%M:%S", time.localtime()) + ": python news updated")
        time.sleep(three_hours_in_seconds)


if __name__ == '__main__':
    if '--help' in sys.argv:
        _print_help()
    else:
        auto_mode = False
        if '--auto' in sys.argv:
            auto_mode = True
            sys.argv.remove('-auto')
        if len(sys.argv) > 2:
            _print_help()
        else:
            db_filename = sys.argv[1] if len(sys.argv) == 2 else 'python_news_db.json'
            update_news_with_console_output(auto_mode, db_filename)
