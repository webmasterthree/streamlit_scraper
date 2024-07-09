import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import pymongo
import json
import os
from .scraper.scraper import crawl_web
from datetime import datetime

now = datetime.now()
date_time = now.strftime("%Y-%m-%d_%H-%M-%S")


def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    # driver = webdriver.Chrome()
    return driver


def scraper_main(urls, info):
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    # client = pymongo.MongoClient("localhost", 27017)
    client = pymongo.MongoClient("mongodb://root:Edubild_123@mongodb:27017")
    db = client["scraped"]
    collection = db["scrap_info"]
    history = db["history"]
    result = history.insert_one(
        {"date_and_time": date_time, "info": f"Data from {info}"}
    )
    driver = create_driver()

    for url in urls:
        crawl_web(driver, collection, url, result.inserted_id)


# if __name__ == "__main__":
#     urls = ["https://edubild.com/", "https://www.kamtech.in/"]
#     scraper_main(urls)
