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


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}
start_url='https://www.booking.com/reviews/sg/hotel/rasa-sentosa-resort-by-the-shangri-la.en-gb.html?aid=356980&label=gog235jc-1BEgdyZXZpZXdzKIICOOgHSDNYA2jJAYgBAZgBCbgBF8gBDNgBAegBAYgCAagCA7gCgrj9mAbAAgHSAiQ1NjY2NDdjNy03NjEzLTRiNjEtYjQ1OC04MDk1Y2M2MzhlYjLYAgXgAgE&sid=db2ad224c338fc25044fbb34d57e5a03'

s=Service(r'C:\Users\Reynaldi\Desktop\chromedriver.exe') #Local file location for chromedriver.exe to use selenium to use the webbrowser

driver = webdriver.Chrome(service=s) #To get the chrome service started
driver.get(start_url) #To go to the url
time.sleep(1)
#driver.find_element(By.CLASS_NAME,"hp-review-score-cta-container-remote").click()
#time.sleep(2)
page_source=driver.page_source
with open('pagetestzz.html', 'w+',encoding="utf-8") as f:
    f.write(driver.page_source) #Saves and writes the page source or html code locally

while True:

    newurl=driver.current_url
    print(newurl)
    driver.get(newurl)
    page_source=driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')  # Parses the data/html code

    # html_text = soup.get_text() #Retrieves all the text (Don't use this)
    testing = soup.find_all('p', attrs={'class': 'review_pos'})

    categories_pos = [t.get_text(strip=True) for t in soup.find_all('p', attrs={
        'class': 'review_pos'})]  # Retrieves all text within the reviewBody so mixes both positive and negative and saves them in a list
    categories_neg = [t.get_text(strip=True) for t in soup.find_all('p', attrs={
        'class': 'review_neg'})]  # ('p' is for class type, followed by name of class in ,attrs={'class' : 'here'}
    hotelname = [t.get_text(strip=True) for t in soup.find_all('a', attrs={'class': 'standalone_header_hotel_link'})]
    hoteladdress = [t.get_text(strip=True) for t in soup.find_all('p', attrs={'class': 'hotel_address'})]
    review_score = [t.get_text(strip=True) for t in soup.find_all('span', attrs={'class': 'review-score-badge'})]
    review_score = review_score[1::]
    # test_texxt=soup.find_all("span", itemprop="reviewBody") #Retrieves all text within the reviewBody so mixes both positive and negative
    combined = zip(review_score, categories_pos)

    'print output to csv'

    with open(hotelname[0] + ".csv", "a",encoding="utf-8") as csvFile:
        fieldnames = ['id', 'review', 'review-score']
        writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        for item in combined:
            writer.writerow({'id': hotelname[0], 'review': item[1], 'review-score': item[0]})
    csvFile.close()
    combined=0
    review_score=0
    categories_pos=0
    driver.find_element("xpath","//*[contains(@id, 'review_next_page_link')]").click()

driver.quit()
'Ignore below its what im working on - ruifeng'

# from geopy.geocoders import Nominatim
#
# loc = Nominatim(user_agent='GetLoc')
# getLoc = loc.geocode(hoteladdress[0])
# print(getLoc.address)
# print(getLoc.latitude)
# print(getLoc.longitude)
#


# df = pd.read_csv('datafiniti_hotel_reviews (2) - Copy.csv', encoding = "ISO-8859-1") 'encoding to read edited csv file'
#
# reviewtext = df['reviews_text']
# reviewrating = df['reviews_rating']
#
#
# 'Histogram'
# import plotly.express as px
# fig = px.histogram(df, x='reviews_rating')
# fig.update_layout(title_text='Review rating')
# fig.show()


