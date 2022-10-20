import time
import csv
import requests
import scrapy
from bs4 import BeautifulSoup
import pandas as pd
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

input_url = 'https://www.booking.com/reviews/sg/hotel/the-barracks-by-far-east-hospitality.en-gb.html?aid=356980&label=gog235jc-1FEgdyZXZpZXdzKIICOOgHSDNYA2jJAYgBAZgBCbgBF8gBDNgBAegBAfgBDYgCAagCA7gCgrj9mAbAAgHSAiQ1NjY2NDdjNy03NjEzLTRiNjEtYjQ1OC04MDk1Y2M2MzhlYjLYAgbgAgE&sid=248efadb06977d69b94338011302293d'


def review_check_pos(positive_review):
    pos_review = [t.get_text(strip=True) for t in positive_review.find_all('p', attrs={
        'class': 'review_pos'})]
    if pos_review == []:
        return False
    elif pos_review != []:
        return True


def review_check_neg(negative_review):
    neg_review = [t.get_text(strip=True) for t in negative_review.find_all('p', attrs={
        'class': 'review_neg'})]
    if neg_review == []:
        return False
    elif neg_review != []:
        return True


def scrape_cat(x):
    writeheader = True
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }
    start_url = x

    s = Service(
        r'C:\Users\Reynaldi\Desktop\chromedriver.exe')  # Local file location for chromedriver.exe to use selenium to use the webbrowser
    driver = webdriver.Chrome(service=s)  # To get the chrome service started
    driver.get(start_url)  # To go to the url
    time.sleep(1)
    # driver.find_element(By.CLASS_NAME,"hp-review-score-cta-container-remote").click()
    # time.sleep(2)
    page_source = driver.page_source
    with open('pagetestzz.html', 'w+', encoding="utf-8") as f:
        f.write(driver.page_source)  # Saves and writes the page source or html code locally
    soup = BeautifulSoup(page_source, 'lxml')
    review_score = [t.get_text(strip=True) for t in
                    soup.find_all('span', attrs={'class': 'review-score-badge'})]
    overall_review = review_score[0]
    scoresz = [t.get_text(strip=True) for t in soup.find_all('p', attrs={'class': 'review_score_value'})]


    combined = zip([overall_review],[scoresz[0]], [scoresz[1]],[scoresz[2]],[scoresz[3]],[scoresz[4]],[scoresz[5]],[scoresz[6]])

    with open("overview.csv", "a", encoding="utf-8", newline='') as csvFile:
        fieldnames = ['overall', 'cleanliness', 'comfort', 'location', 'facilities', 'staff',
                      'value_for_money','Free_wifi']
        writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        if writeheader == True:
            writer.writeheader()
            writeheader = False
        for item in combined:
            writer.writerow(
                {'overall': item[0], 'cleanliness': item[1], 'comfort': item[2], 'location': item[3],
                 'facilities': item[4], 'staff': item[5], 'value_for_money': item[6],'Free_wifi': item[7]})
    csvFile.close()
    driver.quit()


scrape_cat(input_url)

