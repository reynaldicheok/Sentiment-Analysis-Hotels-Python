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

def scrapemulti(x,y):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }

    # start_url='https://www.booking.com/reviews/sg/hotel/rasa-sentosa-resort-by-the-shangri-la.en-gb.html?aid=356980&label=gog235jc-1BEgdyZXZpZXdzKIICOOgHSDNYA2jJAYgBAZgBCbgBF8gBDNgBAegBAYgCAagCA7gCgrj9mAbAAgHSAiQ1NjY2NDdjNy03NjEzLTRiNjEtYjQ1OC04MDk1Y2M2MzhlYjLYAgXgAgE&sid=db2ad224c338fc25044fbb34d57e5a03'
    #review_start_url = 'https://www.booking.com/reviews/sg/city/singapore.en-gb.html?aid=356980&label=gog235jc-1FEgdyZXZpZXdzKIICOOgHSDNYA2jJAYgBAZgBCbgBF8gBDNgBAegBAfgBDYgCAagCA7gCgrj9mAbAAgHSAiQ1NjY2NDdjNy03NjEzLTRiNjEtYjQ1OC04MDk1Y2M2MzhlYjLYAgbgAgE'
    review_start_url = x
    s = Service(
        r'C:\Users\user\PycharmProjects\SITProject\chromedriver.exe')  # Local file location for chromedriver.exe to use selenium to use the webbrowser

    driver = webdriver.Chrome(service=s)  # To get the chrome service started
    driver.get(review_start_url)  # To go to the url
    time.sleep(1)
    # driver.find_element(By.CLASS_NAME,"hp-review-score-cta-container-remote").click()
    # time.sleep(2)
    page_source = driver.page_source
    with open('pagetestzz.html', 'w+', encoding="utf-8") as f:
        f.write(driver.page_source)  # Saves and writes the page source or html code locally

    links = []
    while True:
        try:
            review_url = driver.current_url
            print(review_url)
            driver.get(review_url)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'lxml')  # Parses the data/html code

            for link in soup.find_all(
                    class_="rlp-main-hotel-review__review_link"):  # to append the link that is retrieved from html
                review_link = link.a.get('href')
                links.append(
                    'https://www.booking.com' + review_link)  # because the html containing the link does not have the https link
            print(links)
            driver.find_element(By.CSS_SELECTOR, "a.rlp-main-pagination__btn-txt--next").click()
            writeheader = True
        except:
            print("error")
            break

    for x in range(y):
        driver.get(links[x])
        while True:
            try:
                newurl = driver.current_url
                print(newurl)
                checkString = links[x]

                driver.get(newurl)

                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'lxml')  # Parses the data/html code

                # html_text = soup.get_text() #Retrieves all the text (Don't use this)
                testing = soup.find_all('p', attrs={'class': 'review_pos'})
                # categories_pos = [t.get_text(strip=True) for t in soup.find_all('p', attrs={
                #    'class': 'review_pos'})]  # Retrieves all text within the reviewBody so mixes both positive and negative and saves them in a list
                # categories_neg = [t.get_text(strip=True) for t in soup.find_all('p', attrs={
                #    'class': 'review_neg'})]  # ('p' is for class type, followed by name of class in ,attrs={'class' : 'here'}
                hotelname = [t.get_text(strip=True) for t in
                             soup.find_all('a', attrs={'class': 'standalone_header_hotel_link'})]
                hoteladdress = [t.get_text(strip=True) for t in soup.find_all('p', attrs={'class': 'hotel_address'})]
                review_score = [t.get_text(strip=True) for t in
                                soup.find_all('span', attrs={'class': 'review-score-badge'})]
                review_score = review_score[1::]

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
                        review_pos.append(["No positive review"])
                    if review_check_neg(review_fix_test) == True:
                        review_neg.append(neg_review)
                    if review_check_neg(review_fix_test) == False:
                        review_neg.append(["No negative review"])
                review_negz = [item for sublist in review_neg for item in sublist]
                review_negz = [item.replace('\n', '') for item in review_negz]

                review_posz = [item for sublist in review_pos for item in sublist]
                review_posz = [item.replace('\n', '') for item in review_posz]

                'Grab just postal code'
                postalcodecountry = hoteladdress[0].split(' ')
                count = ''
                postalcode = ''
                postalcodefinal = ''
                for x in postalcodecountry:  # Check array of split text for 6 digit postal code
                    count = sum(map(str.isdigit, x))
                    if count >= 5:
                        postalcode = x
                postalcodefinal = ''.join(c for c in str(postalcode) if c.isdigit())

                from geopy.geocoders import Nominatim

                geolocator = Nominatim(user_agent="geoapiExercises")
                location = geolocator.geocode('Singapore ' + postalcodefinal)
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
                scoreandreview = []
                scorecount = 1

                combined = zip(review_posz, review_negz, updatedscore)

                combined2 = []
                for i in combined:
                    addin = postalcodefinal, getLoc['lat'], getLoc['lon'], i[0], i[1], i[2]
                    combined2.append(addin)

                'print output to csv'

                with open(hotelname[0] + ".csv", "a", encoding="utf-8", newline='') as csvFile:
                    fieldnames = ['id', 'postalcode', 'latitude', 'longitude', 'review_pos', 'review_neg',
                                  'review-score']
                    writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
                    if writeheader == True:
                        writer.writeheader()
                        writeheader = False
                    for item in combined2:
                        writer.writerow(
                            {'id': hotelname[0], 'postalcode': item[0], 'latitude': item[1], 'longitude': item[2],
                             'review_pos': item[3], 'review_neg': item[4], 'review-score': item[5]})

                with open('datafiniti_hotel_reviews (2) - Copy.csv', "a", encoding="utf=8", newline='') as csvFile:
                    fieldnames = ['id', 'dateadded', 'dateupdated', 'address', 'categories', 'primarycategories',
                                  'city',
                                  'country',
                                  'keys', 'latitude', 'longitude', 'name', 'postalcode', 'province', 'reviews_date',
                                  'reviews_dateseen', 'reviews_rating', 'reviews_sourceurls', 'reviews_text']
                    writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
                    for item in combined2:
                        writer.writerow(
                            {'id': '', 'dateadded': '', 'dateupdated': '', 'address': '', 'categories': '',
                             'primarycategories': '',
                             'city': '', 'country': '', 'keys': '', 'latitude': item[1], 'longitude': item[2],
                             'name': hotelname[0], 'postalcode': item[0], 'province': '', 'reviews_date': '',
                             'reviews_dateseen': '', 'reviews_rating': item[5], 'reviews_sourceurls': '',
                             'reviews_text': item[3] + item[4]})
                csvFile.close()
                combined = 0
                review_score = 0
                categories_pos = 0

                driver.find_element("xpath", "//*[contains(@id, 'review_next_page_link')]").click()
            except:
                print("fail or end of pages")
                break

    driver.quit()
    hotel_csv_name = hotelname[0] + ".csv"
    return hotel_csv_name

scrapemulti('https://www.booking.com/reviews/sg/city/singapore.en-gb.html?aid=356980&sid=248efadb06977d69b94338011302293d&label=gog235jc-1FEgdyZXZpZXdzKIICOOgHSDNYA2jJAYgBAZgBCbgBF8gBDNgBAegBAfgBDYgCAagCA7gCgrj9mAbAAgHSAiQ1NjY2NDdjNy03NjEzLTRiNjEtYjQ1OC04MDk1Y2M2MzhlYjLYAgbgAgE',15)