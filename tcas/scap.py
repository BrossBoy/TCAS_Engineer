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

# eng_list = driver.find_elements(By.XPATH, '//*[@id="results"]/ul/li')

course = driver.find_elements(By.XPATH, '//*[@id="results"]/ul/li/a/h3/span')
course_type = driver.find_elements(By.XPATH, '//*[@id="results"]/ul/li/a/h3/small')
engineerings = [f"{i.text} {j.text}" for i, j in zip(course, course_type)]
universitys = [
    i.text
    for i in driver.find_elements(By.XPATH, '//*[@id="results"]/ul/li/a/span/span')
]
links = [
    i.get_attribute("href")
    for i in driver.find_elements(By.XPATH, '//*[@id="results"]/ul/li/a')
]

unique_university = set(universitys)

print(len(course), len(course_type), len(universitys))
# driver.get(links[0])
# time.sleep(1)
# term_fees = driver.find_elements(By.XPATH, '//*[@id="overview"]/dl/dd')

driver.close()
