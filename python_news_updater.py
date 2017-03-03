import sys
import time
from python_news_update_manager import PythonNewsUpdateManager
from habrahabr_news_loader import HabraHabrNewsLoader
from linux_org_news_loader import LinuxOrgNewsLoader
from tproger_news_loader import TProgerNewsLoader
from vk_news_loader import VkNewsLoader

# TODO add logger, control errors in modules
def configure_manager(db_filename):
    manager = PythonNewsUpdateManager(db_filename)
    manager.add_news_loader(HabraHabrNewsLoader())
    manager.add_news_loader(LinuxOrgNewsLoader())
    manager.add_news_loader(TProgerNewsLoader())
    manager.add_news_loader(VkNewsLoader())
    return manager

if __name__ == '__main__':
    auto_mode = False
    if '-auto' in sys.argv:
        auto_mode = True
        sys.argv.remove('-auto')
    if len(sys.argv) > 2:
        print("Usage: python python_news_updater [db_filename] [-auto]")
        print("-auto parameter makes program to stay "
              "in memory and update news every 3 hours")
    db_filename = sys.argv[1] if len(sys.argv) >= 2 else 'python_news_db.json'
    manager = configure_manager(db_filename)
    if not auto_mode:
        manager.update_news()
        print("Done!")
    else:
        print("News manager will update news every 3 hours. Press Ctrl+C to exit")
        three_hours_in_seconds = 3*60*60
        while True:
            manager.update_news()
            print(time.strftime("%H:%M:%S", time.localtime()) + ": python news updated")
            time.sleep(three_hours_in_seconds)
