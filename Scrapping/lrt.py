from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import requests
import time

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

prevArticles = set()

baseUrl = "https://www.lrt.lt"

f = open("lrt.csv", "w", encoding="utf-8")
writer = csv.DictWriter(f, fieldnames=["content", "category"])
writer.writeheader() 

def removePrefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

def getArticle(subUrl):
    try:
        url =  baseUrl + subUrl
        response = requests.get(url)
        response.encoding = "utf-8"

        soup = BeautifulSoup(response.text, "html.parser")

        articleParts = soup.find_all(class_="article-block__content")

        article = ""

        for part in articleParts:
            article += part.get_text(separator=" ", strip=True)

        article = removePrefix(article, "00:00 | 00:00 00:00 ")
        return article.strip().replace("\n","")
    except:
        return ""

def getArticles(subUrl, category):
    url = baseUrl + subUrl
    driver.get(url)
    time.sleep(2)

    i = 0

    section = driver.find_element(By.CLASS_NAME, "js-news-section")
    
    for i in range(1999):
        try:
            button = section.find_element(By.CLASS_NAME, "section__button")
        except:
            break
        driver.execute_script("arguments[0].click();", button)
        time.sleep(1)


    section_html = section.get_attribute("innerHTML")
    soup = BeautifulSoup(section_html, "html.parser")
    articles = soup.find_all(class_="news__title")
    for article in articles:
        a = article.find("a")
        if a and a.has_attr("href"):
            href = a["href"]

            href = removePrefix(href, baseUrl)
            if(href in prevArticles): continue
            prevArticles.add(href)

            article = getArticle(href)
            if(not article == ""): writer.writerow({"content": article, "category": category})

categories = [
    {"subUrl": "/naujienos/sportas", "tagCategory": "sportas"},
    {"subUrl": "/naujienos/sveikata", "tagCategory": "mokslas"},
    {"subUrl": "/naujienos/pozicija", "tagCategory": "politika"},
    {"subUrl": "/naujienos/kultura", "tagCategory": "kultūra"},
    {"subUrl": "/naujienos/muzika", "tagCategory": "kultūra"},
    {"subUrl": "/tema/politika", "tagCategory": "politika"},
    {"subUrl": "/tema/seimas", "tagCategory": "politika"},
    {"subUrl": "/tema/rinkimai", "tagCategory": "politika"},
    {"subUrl": "/tema/rusijos-karas-pries-ukraina", "tagCategory": "politika"},
    {"subUrl": "/tema/it", "tagCategory": "technologija"},
    {"subUrl": "/tema/technologijos", "tagCategory": "technologija"},
    {"subUrl": "/tema/mokslas", "tagCategory": "mokslas"},
    {"subUrl": "/tema/biologija", "tagCategory": "mokslas"},
    {"subUrl": "/tema/chemija", "tagCategory": "mokslas"},
    {"subUrl": "/tema/fizika", "tagCategory": "mokslas"},
    {"subUrl": "/tema/matematika", "tagCategory": "mokslas"},
    {"subUrl": "/tema/sociologija", "tagCategory": "mokslas"},
    {"subUrl": "/tema/teatras", "tagCategory": "kultūra"},
    {"subUrl": "/tema/filmai", "tagCategory": "kultūra"},
    {"subUrl": "/tema/filmas", "tagCategory": "kultūra"},
    {"subUrl": "/tema/literatura", "tagCategory": "kultūra"},
    {"subUrl": "/tema/zaidimai", "tagCategory": "kultūra"},
]

for category in categories:
    print(category["subUrl"])
    getArticles(category["subUrl"], category["tagCategory"])

driver.quit()
f.close()