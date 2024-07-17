from selenium import webdriver
from selenium.webdriver.common.by import By
import time

url = "https://course.mytcas.com/"
driver = webdriver.Chrome()
driver.get(url)
time.sleep(3)
driver.find_element(By.ID, "search")
search_bar = driver.find_element("id", "search")
search_bar.send_keys("คณะวิศวกรรม")
time.sleep(3)

eng_list = driver.find_elements(By.XPATH, '//*[@id="results"]/ul/li')

engineerings = []
universitys = []
links = []

for i in range(len(eng_list)):
    engineerings.append(
        driver.find_element(
            By.XPATH, f'//*[@id="results"]/ul/li[{i + 1}]/a/h3/span'
        ).text
        + " "
        + driver.find_element(
            By.XPATH, f'//*[@id="results"]/ul/li[{i + 1}]/a/h3/small'
        ).text
    )
    universitys.append(
        driver.find_element(
            By.XPATH, f'//*[@id="results"]/ul/li[{i + 1}]/a/span/span'
        ).text
    )
    links.append(
        driver.find_element(
            By.XPATH, f'//*[@id="results"]/ul/li[{i + 1}]/a'
        ).get_attribute("href")
    )

unique_university = set(universitys)

print(unique_university, len(unique_university))

driver.close()
