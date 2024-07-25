from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
import requests

if __name__ == "__main__":
    url = "https://course.mytcas.com/"
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)
    search_bar = driver.find_element(By.ID, "search")
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

    unique_univer = set(universitys)
    api_key = "google map api"
    univer_lat_long = dict()
    for i in unique_univer:
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={i}&key={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data["results"]:
                location = data["results"][0]["geometry"]["location"]
                print(i, location["lat"], location["lng"])
                univer_lat_long[i] = {"lat": location["lat"], "long": location["lng"]}
            else:
                univer_lat_long[i] = {"lat": "-", "long": "-"}
        else:
            univer_lat_long[i] = {"lat": "-", "long": "-"}

    json_object = json.dumps(dicts, indent=4, ensure_ascii=False)
    with open("data/tcas_data.json", "w", encoding="utf-8") as outfile:
        outfile.write(json_object)

    json_object = json.dumps(univer_lat_long, indent=4, ensure_ascii=False)
    with open("data/univer_lat_long.json", "w", encoding="utf-8") as outfile:
        outfile.write(json_object)
