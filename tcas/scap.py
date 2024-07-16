from selenium import webdriver
from selenium.webdriver.common.by import By
import time

url = "https://course.mytcas.com/"
driver = webdriver.Chrome()
driver.get(url)
time.sleep(5)
driver.find_element(By.ID, "search")
search_bar = driver.find_element("id", "search")
search_bar.send_keys("คณะวิศวกรรม")
time.sleep(10)
# print(driver.title)
