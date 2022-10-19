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
from geopy.extra.rate_limiter import RateLimiter

input_url = 'https://www.booking.com/reviews/sg/hotel/four-season-singapore.en-gb.html?aid=356980&label=gog235jc-1FEgdyZXZpZXdzKIICOOgHSDNYA2jJAYgBAZgBCbgBF8gBDNgBAegBAfgBDYgCAagCA7gCgrj9mAbAAgHSAiQ1NjY2NDdjNy03NjEzLTRiNjEtYjQ1OC04MDk1Y2M2MzhlYjLYAgbgAgE&sid=0592c1baed62f1328376ae7ea3a086ed&customer_type=total&hp_nav=0&old_page=0&order=featuredreviews&page=1&r_lang=en&rows=75&'


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

def scrapeone(x):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }
    start_url = x

    s = Service(
        r'D:\School\INF1002\Week2\chromedriver.exe')  # Local file location for chromedriver.exe to use selenium to use the webbrowser

    driver = webdriver.Chrome(service=s)  # To get the chrome service started
    driver.get(start_url)  # To go to the url
    time.sleep(1)
    # driver.find_element(By.CLASS_NAME,"hp-review-score-cta-container-remote").click()
    # time.sleep(2)
    page_source = driver.page_source
    with open('pagetestzz.html', 'w+', encoding="utf-8") as f:
        f.write(driver.page_source)  # Saves and writes the page source or html code locally

    writeheader = True
    while True:
        try:
            newurl = driver.current_url
            print(newurl)
            driver.get(newurl)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'lxml')  # Parses the data/html code

            hotelname = [t.get_text(strip=True) for t in
                         soup.find_all('a', attrs={'class': 'standalone_header_hotel_link'})]
            hoteladdress = [t.get_text(strip=True) for t in soup.find_all('p', attrs={'class': 'hotel_address'})]
            review_score = [t.get_text(strip=True) for t in
                            soup.find_all('span', attrs={'class': 'review-score-badge'})]
            overall_review = [review_score[0]]
            scoresz = [t.get_text(strip=True) for t in soup.find_all('p', attrs={'class': 'review_score_value'})]
            review_score = review_score[1::]
            # test_texxt=soup.find_all("span", itemprop="reviewBody") #Retrieves all text within the reviewBody so mixes both positive and negative

            review_fix = [t.get_text for t in soup.find_all("div", attrs={
                "class": "review_item_review_content"})]  # Retrieves all text within the reviewBody so mixes both positive and negative
            review_pos = []
            review_neg = []
            for reviews in review_fix:

                review_fix_test = BeautifulSoup(str(reviews), 'lxml')
                pos_review = [t.get_text(strip=True) for t in review_fix_test.find_all('p', attrs={
                    'class': 'review_pos'})]
                neg_review = [t.get_text(strip=True) for t in review_fix_test.find_all('p', attrs={
                    'class': 'review_neg'})]
                if review_check_pos(review_fix_test) == True:
                    review_pos.append(pos_review)
                if review_check_pos(review_fix_test) == False:
                    review_pos.append([""])
                if review_check_neg(review_fix_test) == True:
                    review_neg.append(neg_review)
                if review_check_neg(review_fix_test) == False:
                    review_neg.append([""])
            review_negz = [item for sublist in review_neg for item in sublist]
            review_negz = [item.replace('\n', '') for item in review_negz]

            review_posz = [item for sublist in review_pos for item in sublist]
            review_posz = [item.replace('\n', '') for item in review_posz]

            'Grab just postal code'
            postalcodecountry = hoteladdress[0].split(' ')
            postalcode = ''
            for x in postalcodecountry:  # Check array of split text for 6 digit postal code
                count = sum(map(str.isdigit, x))
                if count >= 5:
                    postalcode = x
            postalcodefinal = ''.join(c for c in str(postalcode) if c.isdigit())

            from geopy.geocoders import Nominatim

            geolocator = Nominatim(user_agent="geoapiExercises")
            location = geolocator.geocode(postalcodefinal+ ' SG', exactly_one=True, timeout=60)
            getLoc = location.raw

            updatedscore = []
            # Append Review Score together with Review
            review_score = [float(x) for x in review_score]
            review_score = [int(x) for x in review_score]


            for x in review_score:
                if int(x) < 5:
                    updatedscore.append(1)
                if int(x) == 6:
                    updatedscore.append(2)
                if int(x) == 7:
                    updatedscore.append(3)
                if int(x) == 8:
                    updatedscore.append(4)
                if int(x) == 9:
                    updatedscore.append(5)
                if int(x) == 10:
                    updatedscore.append(5)


            combined = zip(review_posz, review_negz, updatedscore,overall_review,scoresz[0],scoresz[1],scoresz[2],scoresz[3],scoresz[4],scoresz[5],scoresz[6])

            combined2 = []
            for i in combined:
                addin = postalcodefinal, getLoc['lat'], getLoc['lon'], i[0], i[1], i[2]
                combined2.append(addin)

            'print output to csv'

            with open(hotelname[0] + ".csv", "a", encoding="utf-8", newline='') as csvFile:
                fieldnames = ['hotelname', 'postalcode', 'latitude', 'longitude', 'review_pos', 'review_neg', 'review_text', 'review-score','overall_score','cleanliness','comfort','location','facilities','staff','value_for_money','Free_Wifi']
                writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
                if writeheader == True:
                    writer.writeheader()
                    writeheader = False
                for item in combined2:
                    writer.writerow(
                        {'hotelname': hotelname[0], 'postalcode': item[0], 'latitude': item[1], 'longitude': item[2],
                         'review_pos': item[3], 'review_neg': item[4], 'review_text': str(item[3]) +' '+ str(item[4]),'review-score': item[5],
                         'overall_score': item[6],'cleanliness': item[7],'comfort': item[8],'location': item[9],'facilities': item[10],
                         'staff': item[11],'value_for_money': item[12],'Free_Wifi': item[13]})

            with open('SingaporeHotel.csv', "a", newline='', encoding="utf-8") as csvFile:
                fieldnames = ['hotelname', 'postalcode', 'latitude', 'longitude', 'review_pos', 'review_neg','review_text', 'review-score']
                writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
                for item in combined2:
                    writer.writerow(
                        {'hotelname': hotelname[0], 'postalcode': item[0], 'latitude': item[1], 'longitude': item[2],
                         'review_pos': item[3], 'review_neg': item[4], 'review_text': str(item[3]) + ' ' + str(item[4]),
                         'review-score': item[5]})
            csvFile.close()
            driver.find_element("xpath", "//*[contains(@id, 'review_next_page_link')]").click()
        except:
            print("fail or end of pages")
            break
    hoteloutputcsv = hotelname[0] + ".csv"
    return hoteloutputcsv
    driver.quit()


test = scrapeone(input_url)

