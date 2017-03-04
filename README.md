# pyPythonNewsBot

## What is this?  
This project is designed for configuring Telegram bot that answer user's command ```/python_news``` with actual news about Python. Modules and class structure allow you to easily load news from different sources. By default, news is loaded from [vk.com](https://vk.com), [habrahabr.ru](https://habrahabr.ru/hub/python/), [tproger.ru](https://tproger.ru/tag/python/) and [linux.org](https://www.linux.org.ru/tag/python?section=1)  

## How to use

### python_news_update.py [news_db_filename] [--auto] 
This script appends latest news to ```news_db_filename``` file. If file does not exist, then news since previous midnight are loaded. By default, ```news_default_filename``` is ```python_news_db.json```  
Additional parameter ```--auto``` forces program to stay in memory and update news every 3 hours  

### python_news_telegram_bot.py [news_db_filename]
This script starts telegram bot that loads news from ```news_db_filename```(default ```python_news_db.json```) file and reports random news of the latest day to user. Bot use news only once, so if all news are reported, then the latest news are loaded. If this operation fails, then ```'Sorry, no actual news available. Try later'``` is reported.  
Finally, user receives the message with short info about news and link to source  
You must set environment variable TELEGRAM_API_TOKEN to you telegram bot's token before start!!! Read more about telegram bots [here](https://core.telegram.org/bots)  

#####NOTE: during the work of these programs, it may be necessary to set enveronment variable ```VK_API_KEY``` to your vk api token (you can get it [here](https://vk.com/dev/access_token))

## How to install  
All dependencies are listed in ```requirements.txt```. To import it, just run ```pip install -r requirements.txt``` 

## What is under the hood?
Updating news is based on class heirarchy starting with abstract class ```PythonNewsLoader``` with abstract functions:  
```
def clear_cache(self)
def update_news(self)
def move_next(self)
def get_current_article_datetime(self)
def get_current_article_title(self)
def get_current_article_description(self)
def get_current_article_link(self)
```
It implements [Iterator pattern](https://en.wikipedia.org/wiki/Iterator_pattern) and iterate articles until not-actual article is reached. It has two inheritors - ```VkNewsLoader``` and abstract ```PythonNewsHtmlLoader```. ```VkNewsLoader``` searches for posts with keyword ```#python``` and filters posts with pre-defined spam word combinations. ```PythonNewsHtmlLoader``` is designed to work with html page parsers, so it's inheritors must specify base news downloading url and implement this list of functions: 
```
def parse_html_page_to_articles(self, html_page)
def get_next_page_link_from_html(self, html_page)
def get_current_article_datetime(self)
def get_current_article_title(self)
def get_current_article_description(self)
def get_current_article_link(self)
```
```HabraHabrNewsLoader, LinuxOrgNewsLoader, TProgerNewsLoader``` classes implement ```PythonNewsHtmlLoader``` abstract class and load news from different websites  
 ```PythonNewsLoader```'s function ```get_news(datetime_of_latest_article)``` returns collection of news from some source. This function is called in ```PythonNewsUpdateManager``` class, that allows you to add multiple loaders and get actual news by one call of funtion ```update_news_in_db()```. It also uses ```PythonNewsDbManager``` that reads and writes articles to database file. Passing some logger to ```PythonNewsLoader```'s constructor allows you to log it's work  
 ```python_news_telegram_bot``` module contains functions that controls the telegram bot. On command ```/python_news``` the bot is looking for actual news that was not reported to the asking user and updates news using the above classes if needed. If no news available, the bot reports ```'Sorry, no actual news available. Try later'```  
