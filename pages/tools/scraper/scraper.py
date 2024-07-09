from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from .get_items import get_emails, get_phones
from urllib.parse import urljoin, urlparse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import os
# from scraper.write_to_excel import write_to_excel

log_file_path = os.path.abspath('Logs')
# Define the directory and file path
log_file = 'Error_Logs.txt'

# Ensure the directory exists; create if not
if not os.path.exists(log_file_path):
    os.makedirs(log_file_path)

# Combine directory and file to get the full path
log_file_path = os.path.join(log_file_path, log_file)

def crawl_web(driver: webdriver.Chrome, collection, url, history):
    try:
        if url is None or url.strip() == '':
            with open(log_file_path, 'a') as f:
                now = datetime.now()
                date_time = now.strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"{date_time} : URL is None\n")
            return False
    
    except Exception as e:
        print(e)
        return False
    
    try:
        driver.get(url)
        sleep(10)
        html = driver.page_source
        emails = []
        phones = []

        details = {}
        details['link'] = url
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'title')))

        #Fetch the title element
        title_tag = driver.find_element(By.TAG_NAME, 'title')
        title_text = title_tag.get_attribute('textContent')
        details['title'] = title_text
        emails = get_emails(html)

        details['emails'] = emails

        phones = get_phones(html)

        details['phones'] = phones

        all_links = driver.find_elements(By.XPATH, '//a[@href]')
        relevant_links = []
        for link in all_links:
            if 'contact' in link.text.lower() or 'about' in link.text.lower():
                relevant_links.append(link.get_attribute('href'))
                continue

            if 'contact' in link.get_attribute('href').lower() or 'about' in link.get_attribute('href').lower():
                relevant_links.append(link.get_attribute('href'))

                    
        # relevant_links = [link.get_attribute('href') for link in all_links if 'contact' in link.get_text().lower() or 'about' in link.get_text().lower()]
        absolute_links = [urljoin(url, link) for link in relevant_links]
        absolute_links = list(set(absolute_links))
        print("Links: ", absolute_links)
        i = 1
        for link in absolute_links:
            if urlparse(link).netloc != urlparse(url).netloc:
                continue
            driver.get(link)
            sleep(10)
            html = driver.page_source
            emails = get_emails(html)
            phones = get_phones(html)

            if emails != [] or emails != None:
                details['emails'] += emails
            if phones != [] or phones != None:
                details['phones'] += phones

            i += 1

        details['emails'] = list(set(details['emails']))
        details['phones'] = list(set(details['phones']))
        details['history'] = history

        print("Scrapped Info: ", details)

        # write_to_excel(details)


        collection.insert_one(details)

 
        return True

    except Exception as e:
        print(e)
        with open(log_file_path, 'a') as f:
            now = datetime.now()
            date_time = now.strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{date_time} : {e}\n")
        return False
    
if __name__ == "__main__":
    crawl_web()