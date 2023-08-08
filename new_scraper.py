from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

# NASA Exoplanet URL
START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"

# Webdriver
browser = webdriver.Chrome()
browser.get(START_URL)

time.sleep(10)

new_planets_data = []

def scrape_more_data(hyperlink):
    print(hyperlink)
    
    ## ADD CODE HERE ##
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content, 'html.parser')
        temp_list = []
        for tr_tag in soup.find_all("tr", attrs={"class", "fact_row"}):
            td_tags = tr_tag.find_all('td')
            for td_tag in td_tags:
                try:
                    if index == 1:
                        detection_method = td_tag.find_all('div', attrs = {'class', 'value'}).find_all('a')
                        temp_list.append(detection_method[0].contents[0])
                    else:
                        temp_list.append(td_tag.find_all('div', attrs = {'class', 'value'})[0].contents[0])
                except:
                    temp_list.append('')
            new_planets_data.append(temp_list)
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)
        





planet_df_1 = pd.read_csv("updated_scraped_data.csv")

# Call method
for index, row in planet_df_1.iterrows():

     ## ADD CODE HERE ##
    
     # Call scrape_more_data(<hyperlink>)
    scrape_more_data(row[6])
    print(f"Data Scraping at hyperlink {index+1} completed")

print(new_planets_data)

# Remove '\n' character from the scraped data
scraped_data = []

for row in new_planets_data:
    replaced = []
    ## ADD CODE HERE ##
    for element in row:
        element = element.replace('\n', '')
        replaced.append(element)
    scraped_data.append(replaced)

print(scraped_data)

headers = ["planet_type","discovery_date", "mass", "planet_radius", "orbital_radius", "orbital_period", "eccentricity", "detection_method"]

new_planet_df_1 = pd.DataFrame(scraped_data,columns = headers)

# Convert to CSV
new_planet_df_1.to_csv('new_scraped_data.csv', index=True, index_label="id")
