import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Load the website
alamatSitus = 'https://www.tiktok.com'
pathEdge = r"c:\Users\user\Documents\msedgedriver.exe"  # Path to the Edge driver

# Customize the browser display
browser_options = Options()
browser_options.add_argument("--disable-infobars")
browser_options.add_argument("--start-maximized")

# Set capabilities explicitly
capabilities = {
    "browserName": "MicrosoftEdge",
    "version": "",
    "platform": "ANY",
    "ms:edgeOptions": {
        "args": ["--disable-infobars", "--start-maximized"]
    }
}

# Initialize the WebDriver with the Service class
edge_service = EdgeService(executable_path=pathEdge)
driver = webdriver.Edge(service=edge_service, options=browser_options)


driver.get(alamatSitus)
wait = WebDriverWait(driver, 10)

# Search for the hashtag
tagarSearch = '#kucinglucu'
element = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div/form/input")
element.send_keys(tagarSearch)
element.send_keys(Keys.ENTER)

time.sleep(5)

# Handling modal or pop-up (if any)
ii = 0
while ii < 1:
    try:
        driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div[1]/div[1]").click()
        ii = 1
    except:
        ii = 0
        time.sleep(5)

# Load More
i = 0
while i < 1:
    try:
        next_story = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div/div[1]/div[3]"))
        )
        next_story.click()
        time.sleep(2)
        i = 1
    except:
        i = 0
        time.sleep(5)

# Data html page tiktok dari beautifulsoup4
html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
soup = BeautifulSoup(html, 'html.parser')

# Scraping data tiktok
judul_tiktok, link_tiktok, username = [], [], []
limit = 1

# Judul
for judul in soup.find_all('div', class_='tiktok-leylhp-DivContainer e1cg0wnj0'):
    judul_tiktok.append(judul.text)

# Link
for link in soup.find_all('div', class_='tiktok-yz6ijl-DivWrapper e1cg0wnj1'):
    link_tiktok.append(link.a['href'])

# Username
for user in soup.find_all('p', class_='tiktok-2zn17v-PUniqueId etrd4pu6'):
    username.append(user.text)

# SAVE DATA
listCols = ['Judul_Tiktok', 'Link_Tiktok', 'Username']
dict_data = dict(zip(listCols, [judul_tiktok, link_tiktok, username]))

# Save data to JSON file
with open('dataTiktok.json', 'w') as fp:
    json.dump(dict_data, fp)

# Convert the dictionary to a DataFrame
df = pd.DataFrame(dict_data)

# Display the DataFrame
print(df.head(1))

# Save data to CSV file
df.to_csv('scrape.csv', index=False)

# Close the WebDriver
driver.quit()
