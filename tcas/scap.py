from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

url = "https://course.mytcas.com/"
driver = webdriver.Chrome()
driver.get(url)
time.sleep(3)
driver.find_element(By.ID, "search")
search_bar = driver.find_element("id", "search")
search_bar.send_keys("วิศวกรรม")
time.sleep(3)

universitys = [
    i.text
    for i in driver.find_elements(By.XPATH, '//*[@id="results"]/ul/li/a/span/span')
]
links = [
    i.get_attribute("href")
    for i in driver.find_elements(By.XPATH, '//*[@id="results"]/ul/li/a')
]

dicts = dict()
for i in range(len(universitys)):
    print(i, links[i])
    driver.get(links[i])
    time.sleep(2)
    details = driver.find_elements(By.XPATH, '//*[@id="overview"]/dl/dt')
    sub_details = driver.find_elements(By.XPATH, '//*[@id="overview"]/dl/dd')
    name = driver.find_element(
        By.XPATH, '//*[@id="root"]/main/div[2]/div/span/span/h1'
    ).text
    detail = dict()
    for j in range(len(details)):
        detail[details[j].text] = sub_details[j].text
    dicts[f"eng{i}"] = {
        "name": name,
        "univer": universitys[i],
        "detail": detail,
    }


driver.close()

json_object = json.dumps(dicts, indent=4, ensure_ascii=False)
with open("data/tcas_data.json", "w", encoding="utf-8") as outfile:
    outfile.write(json_object)
