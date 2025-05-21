from bs4 import BeautifulSoup
import csv
import requests

prevArticles = set()

f = open("technologijos.csv", "w", encoding="utf-8")
writer = csv.DictWriter(f, fieldnames=["content", "category"])
writer.writeheader()

def getArticle(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")

        articleParts = soup.find_all(class_ = "fotoDescription3")[2].descendants
        try:
            intro = soup.find(class_ = "tarpelis_krastuose fotoDescription3")
            articleParts = [intro] + article
        except:
            pass
        article = ""
        prev = ""
        for part in articleParts:
            text = part.get_text(separator=" ", strip=True)
            if(text == prev): continue
            article += text + " "
            prev = text
    
        return article.strip().replace("\n","")
    except:
        return ""

def getArticles(url, category):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
    except:
        return
    try:
        years = soup.find(class_ = "metai_info_td").parent.find_all("a")
        yearIndex = -1
    except: 
        years = []
        yearIndex = -1
    while(True):
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, "html.parser")
        except:
            try:
                nextPageButton = soup.find(class_ = "lygiuoti_desine desine_tarpelis fonas_pilka").find("a")
            except:
                nextPageButton = None
        
            if(nextPageButton == None): 
                yearIndex += 1
                if(yearIndex >= len(years)): break

                url = years[yearIndex]["href"]
                continue

            nextPage = nextPageButton["href"]
            url = nextPage
        
        try:
            articlePart = soup.find_all(class_ = "folder_listing_container_3")[1].find("div")
            articles = articlePart.find_all(style="margin:0px 0px 10px 0px")

            for article in articles:
                a = article.find(class_ = "folder_listing_container_2").find(class_ = "BigTitleRubrikoje").find("a")
                url = a['href']

                if(url in prevArticles): continue
                prevArticles.add(url)

                article = getArticle(url)
                if(not article == ""): writer.writerow({"content": article, "category": category})
        except:
            pass
        
        try:
            nextPageButton = soup.find(class_ = "lygiuoti_desine desine_tarpelis fonas_pilka").find("a")
        except:
            nextPageButton = None
        
        if(nextPageButton == None): 
            yearIndex += 1
            if(yearIndex >= len(years)): break

            url = years[yearIndex]["href"]
            continue

        nextPage = nextPageButton["href"]
        url = nextPage

categories = [
    {"url": "http://www.technologijos.lt/n/zmoniu_pasaulis/menine_kuryba/rubrikos-archyvas", "tagCategory": "kultūra"},
    {"url": "http://www.technologijos.lt/n/technologijos/it/zyme/Kompiuteriniai-zaidimai:-naujienos-ir-pasiekimai?tid=159", "tagCategory": "kultūra"},
    {"url": "http://www.technologijos.lt/n/zmoniu_pasaulis/kaip_mes_gyvename/zyme/Rekordiniai-pasiekimai?tid=2256", "tagCategory": "kultūra"},
    {"url": "http://www.technologijos.lt/n/zmoniu_pasaulis/kaip_mes_gyvename/zyme/Sventes-ir-kitos-isimintinos-progos?tid=5220", "tagCategory": "kultūra"},
    {"url": "http://www.technologijos.lt/n/zmoniu_pasaulis/kaip_mes_gyvename/zyme/Renginiai-sventes-ir-laisvalaikis?tid=9261", "tagCategory": "kultūra"},
    {"url": "http://www.technologijos.lt/n/pasaulio_paslaptys/zyme/Mistika-ir-religija?tid=854", "tagCategory": "kultūra"},
    {"url": "http://www.technologijos.lt/filmai/rubrikos-archyvas", "tagCategory": "kultūra"},
    {"url": "http://www.technologijos.lt/n/zmoniu_pasaulis/zyme/Zmogus-ir-menas?tid=14345", "tagCategory": "kultūra"},
    {"url": "http://www.technologijos.lt/n/zmoniu_pasaulis/zyme/Kulinarijos-pasaulis?tid=16381", "tagCategory": "kultūra"},
    {"url": "http://www.technologijos.lt/n/zmoniu_pasaulis/zyme/Turiningas-laisvalaikis?tid=1731", "tagCategory": "kultūra"},
    {"url": "http://www.technologijos.lt/n/zmoniu_pasaulis/keliaujantiems_po_pasauli/zyme/Lankytinos-vietos?tid=2271", "tagCategory": "kultūra"},
    {"url": "http://www.technologijos.lt/n/pasaulis/zyme/Tradicijos?tid=15510", "tagCategory": "kultūra"},
    {"url": "http://www.technologijos.lt/n/pasaulis/zyme/Religines-organizacijos?tid=11401", "tagCategory": "kultūra"},
    {"url": "http://www.technologijos.lt/n/zmoniu_pasaulis/knygos/zyme/Populiariausios-knygos?tid=10293", "tagCategory": "kultūra"},
    {"url": "http://www.technologijos.lt/n/zmoniu_pasaulis/knygos/zyme/Romanai?tid=6754", "tagCategory": "kultūra"},
    {"url": "http://www.technologijos.lt/n/zmoniu_pasaulis/knygos/zyme/Religines-ir-mistines-tematikos-knygos?tid=13240", "tagCategory": "kultūra"},
    {"url": "http://www.technologijos.lt/n/zmoniu_pasaulis/knygos/zyme/Fantastines-knygos?tid=10612", "tagCategory": "kultūra"},
    {"url": "http://www.technologijos.lt/n/zmoniu_pasaulis/knygos/zyme/Socialines-tematikos?tid=1851", "tagCategory": "kultūra"},
    {"url": "http://www.technologijos.lt/n/zmoniu_pasaulis/kaip_mes_gyvename/zyme/Atostogos?tid=3969", "tagCategory": "kultūra"},
    {"url": "http://www.technologijos.lt/n/zmoniu_pasaulis/kaip_mes_gyvename/zyme/Jaunoji-karta?tid=2669", "tagCategory": "kultūra"},
    {"url": "http://www.technologijos.lt/n/technologijos/rubrikos-archyvas", "tagCategory": "technologija"},
    {"url": "http://www.technologijos.lt/rinka/apzvalgos/rubrikos-archyvas", "tagCategory": "technologija"},
    {"url": "http://www.technologijos.lt/n/zmoniu_pasaulis/knygos/zyme/Technologiju-tematikos?tid=12172", "tagCategory": "technologija"},
    {"url": "http://www.technologijos.lt/n/mokslas/rubrikos-archyvas", "tagCategory": "mokslas"},
    {"url": "http://www.technologijos.lt/n/zmoniu_pasaulis/kaip_mes_gyvename/zyme/Sociologija?tid=4768", "tagCategory": "mokslas"},
    {"url": "http://www.technologijos.lt/n/zmoniu_pasaulis/knygos/zyme/Mokslas-populiariai?tid=2262", "tagCategory": "mokslas"},
    {"url": "http://www.technologijos.lt/n/zmoniu_pasaulis/knygos/zyme/Gamtines-tematikos?tid=2857", "tagCategory": "mokslas"},
    {"url": "http://www.technologijos.lt/n/zmoniu_pasaulis/knygos/zyme/Psichologija?tid=2457", "tagCategory": "mokslas"},
    {"url": "http://www.technologijos.lt/n/zmoniu_pasaulis/knygos/zyme/Geografines-tematikos?tid=8559", "tagCategory": "mokslas"},
    {"url": "http://www.technologijos.lt/n/zmoniu_pasaulis/knygos/zyme/Sveikatingumo-ir-medicinos-tematika?tid=14228", "tagCategory": "mokslas"},
    {"url": "http://www.technologijos.lt/n/zmoniu_pasaulis/kaip_mes_gyvename/zyme/Sociologija?tid=4768", "tagCategory": "mokslas"},
    {"url": "http://www.technologijos.lt/n/pasaulis/zyme/Pasauline-politika?tid=26093", "tagCategory": "politika"},
    {"url": "http://www.technologijos.lt/n/lietuva/zyme/Lietuvos-politika?tid=26091", "tagCategory": "politika"},
    {"url": "http://www.technologijos.lt/n/zmoniu_pasaulis/knygos/zyme/Idealogines-knygos?tid=19207", "tagCategory": "politika"},
    {"url": "http://www.technologijos.lt/zyme?tid=4164&rikiavimas=0&a=0&ystart=&ystop=&tipas=0&tik_rubrikos=0&pp=1", "tagCategory": "sportas"},
]

for category in categories:
    print(category["url"])
    getArticles(category["url"], category["tagCategory"])

f.close()