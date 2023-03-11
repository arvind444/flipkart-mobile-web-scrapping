import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

max_retries = 20
backoff_factor = 0.8

retry_strategy = Retry(
    total=max_retries,
    backoff_factor=backoff_factor,
    status_forcelist=[500, 502, 503, 504]
)

session = requests.Session()
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount('http://', adapter)
session.mount('https://', adapter)

names = []
images = []
stars = []
original_price = []
offer_price = []
rating = []
review = []
ram = []
rom = []
expandable = []
display_detail = []
front_camera = []
back_camera = []
battery_mah = []
processor = []

html_text = session.get("https://www.flipkart.com/search?q=mobiles").text
print("Ready to scrap the mobiles data from flipkart.")
print("")
soup = BeautifulSoup(html_text, "lxml")
total_pages = soup.find("div", class_ = "_2MImiq")
total_page = int(total_pages.span.text.split(" ")[-1])
print("There are {} pages to scrap for mobile data from flipkart website.".format(total_page))
print("")
print("But we are going to scrap first 12 pages!!!")
print("")

for j in range(1, 13):
    html_text = session.get("https://www.flipkart.com/search?q=mobiles&page={}".format(j)).text
    print("Scrapping the page number {}.".format(j))
    soup = BeautifulSoup(html_text, "lxml")
    products = soup.find_all("div", class_ = "_1AtVbE col-12-12")

    if products:    
        for i in products:
            images_url = i.find_all("div", class_ = "_2QcLo-")
            names_url = i.find_all("div", class_ = "_4rR01T")
            star_ratings_url = i.find_all("span", class_ = "_1lRcqv")
            original_prices_url = i.find_all("div", class_ = "_3I9_wc _27UcVY")
            offer_prices_url = i.find_all("div", class_ = "_3tbKJL")
            offer_percentages_url = i.find_all("div", class_ = "_3tbKJL")
            ratings_url = i.find_all("span", class_ = "_2_R_DZ")
            details_url = i.find_all("ul", class_ = "_1xgFaf")
            
            if images_url:
                for i in images_url:
                    try:
                        image_url = i.img["src"]
                        images.append(image_url)
                    except:
                        images.append("Not available")

            if names_url:
                for i in names_url:
                    try:
                        name_url = i.text
                        names.append(name_url)
                    except:
                        names.append("Not available")

            if star_ratings_url:
                for i in star_ratings_url:
                    try:
                        star_rating_url = float(i.div.text)
                        stars.append(star_rating_url)
                    except:
                        stars.append("Not available")

            try:
                if original_prices_url:
                    for i in original_prices_url:
                        try:
                            original_price_url = int(i.text.replace("₹", "").replace(",", ""))
                            original_price.append(original_price_url)
                        except:
                            original_price.append("Not available")
            except:
                original_price.append("Not available")

            try:
                if offer_prices_url:
                    for i in offer_prices_url:
                        try:
                            offer_price_url = int(i.div.div.text.replace("₹", "").replace(",", ""))
                            offer_price.append(offer_price_url)
                        except:
                            offer_price.append("Not available")
            except:
                offer_price.append("Not available")

            if ratings_url:
                for i in ratings_url:
                    try:
                        rating_url = i.span.text.split("&")
                        rating.append(int(rating_url[0].replace("Ratings", "").replace(" \xa0", "").replace(",", "")))
                        review.append(int(rating_url[1].replace("Reviews", "").replace("\xa0", "").replace(",", "")))
                    except:
                        rating.append("Not available")
                        review.append("Not available")

            if details_url:
                for i in details_url:
                    try:
                        detail_url = i.li.text.split("|")
                        if len(detail_url) == 3:
                            ram.append(detail_url[0])
                            rom.append(detail_url[1])
                            expandable.append(detail_url[2])
                        elif len(detail_url) == 2:
                            ram.append(detail_url[0])
                            rom.append(detail_url[1])
                            expandable.append("Not available")
                        elif len(detail_url) == 1:
                            ram.append(detail_url[0])
                            rom.append("Not available")
                            expandable.append("Not available")
                        else:
                            ram.append("Not available")
                            rom.append("Not available")
                            expandable.append("Not available")
                    except:
                        ram.append("Not available")
                        rom.append("Not available")
                        expandable.append("Not available")

            if details_url:
                for i in details_url:
                    try:
                        li_url = i.find_all("li")[1].text
                        display_detail.append(li_url)
                    except:
                        display_detail.append("Not available")

            if details_url:
                for i in details_url:
                    try:
                        li_url = i.find_all("li")[2].text.split("|")
                        if len(li_url) == 2:
                            back_camera.append(li_url[0])
                            front_camera.append(li_url[1])
                        elif len(li_url) == 1:
                            back_camera.append(li_url[0])
                            front_camera.append("No Camera")
                        else:
                            back_camera.append("No Camera")
                            front_camera.append("No Camera")
                    except:
                        back_camera.append("Not available")
                        front_camera.append("Not available")

            if details_url:
                for i in details_url:
                    try:
                        li_url = i.find_all("li")[3].text.split(" ")
                        try:
                            battery = int(li_url[0])
                            battery_mah.append(battery)
                        except:
                            battery_mah.append("Not available")
                    except:
                        battery_mah.append("Not available")

            if details_url:
                for i in details_url:
                    try:
                        li_url = i.find_all("li")[-2].text
                        processor.append(li_url)
                    except:
                        processor.append("Not available")

    print("Mobile datas are scrapped from the page number {}.".format(j))

print("Completed !!!!")

print(len(names))
print(len(original_price))
print(len(offer_price))
print(len(stars))
print(len(rating))
print(len(review))
print(len(ram))
print(len(rom))
print(len(expandable))
print(len(display_detail))
print(len(front_camera))
print(len(back_camera))
print(len(battery_mah))
print(len(processor))
print(len(images))

mobile_data_dictionary = {"Name" : names,
                          "Original_price" : original_price,
                          "Offer_price" : offer_price,
                          "Star_rating" : stars,
                          "Total_rating": rating,
                          "Total_review" : review,
                          "RAM" : ram,
                          "ROM" : rom,
                          "Expandable_memory" : expandable,
                          "Display" : display_detail,
                          "Front_camera" : front_camera,
                          "Back_camera" : back_camera,
                          "Battery_mah" : battery_mah,
                          "Processor" : processor,
                          "Image_url" : images}

mobile_data = pd.DataFrame(mobile_data_dictionary)
print(mobile_data.head())
print(mobile_data.tail())
print(mobile_data.shape)
mobile_data.to_csv("Flipkart_mobile_data.csv")
