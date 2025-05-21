import requests
import re
import csv

headers = {
    "User-Agent": "LithuanianLanguageTagging/1.0 (jonzilysetc@gmail.com)"
}

prevArticles = set()
f = open("wikipedia.csv", "w", encoding="utf-8")
writer = csv.DictWriter(f, fieldnames=["content", "category"])
writer.writeheader() 

def getArticles(category, tag, depth):
    data = getCategoryArticles(category)
    
    for page in data:
        if(page["title"].startswith("Kategorija:")): 
            if(depth > 0): 
                getArticles(page["title"].replace("Kategorija:", ""), tag, depth - 1)
                continue
            else: break
        elif(page["title"].startswith("Vaizdas:")): break
        pageid = page["pageid"]

        if(pageid in prevArticles): continue
        prevArticles.add(pageid)
        article = getArticle(pageid)

        if(article == ""): continue
        writer.writerow({"content": article, "category": tag})

def getCategoryArticles(category):
    try:
        url = "https://lt.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "list": "categorymembers",
            "cmtitle": f"Kategorija:{category}",
            "cmlimit": 100
        }

        data = []
        while(True):
            response = requests.get(url, params=params, headers=headers)
            newData = response.json()
            members = newData.get("query", {}).get("categorymembers", [])
            data.extend(members)

            if "continue" in newData:
                params.update(newData["continue"])
            else:
                break
    
        return data
    except:
        return getCategoryArticles(category)


def getArticle(pageid):
    try:
        url = "https://lt.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "explaintext": True,
            "pageids": pageid
        }
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        pages = data["query"]["pages"]
        page = next(iter(pages.values()))
        article = page.get("extract", "")

        cutPatterns = [
            r"^==+\s*Galerija\s*==+", 
            r"^==+\s*Šaltiniai\s*==+", 
            r"^==+\s*Nuorodos\s*==+",
            r"^==+\s*Išnašos\s*==+",
            r"^==+\s*Bibliografija\s*==+",
            r"^==+\s*Literatūra\s*==+"
        ]

        for pattern in cutPatterns:
            cutLocation = re.search(pattern, article, flags=re.MULTILINE | re.IGNORECASE)
            if cutLocation:
                article = article[:cutLocation.start()]
                break

        return article.strip().replace("\n","")
    except:
        return ""

categories = [
    {"articleCategory": "informatika", "tagCategory": "technologija"},
    {"articleCategory": "technologijos", "tagCategory": "technologija"},
    {"articleCategory": "technologija", "tagCategory": "technologija"},
    {"articleCategory": "inžinerija", "tagCategory": "technologija"},
    {"articleCategory": "politologija", "tagCategory": "politika"},
    {"articleCategory": "lietuvos_politinė_sistema", "tagCategory": "politika"},
    {"articleCategory": "politikai", "tagCategory": "politika"},
    {"articleCategory": "sportas", "tagCategory": "sportas"},
    {"articleCategory": "sportininkai", "tagCategory": "sportas"},
    {"articleCategory": "medicina", "tagCategory": "mokslas"},
    {"articleCategory": "chemija", "tagCategory": "mokslas"},
    {"articleCategory": "biologija", "tagCategory": "mokslas"},
    {"articleCategory": "fizika", "tagCategory": "mokslas"},
    {"articleCategory": "matematika", "tagCategory": "mokslas"},
    {"articleCategory": "socialiniai_mokslai", "tagCategory": "mokslas"},
    {"articleCategory": "kultūra", "tagCategory": "kultūra"},
    {"articleCategory": "menas", "tagCategory": "kultūra"},
    {"articleCategory": "religija", "tagCategory": "kultūra"},
    {"articleCategory": "literatūra", "tagCategory": "kultūra"},
    {"articleCategory": "žaidimai", "tagCategory": "kultūra"},
    {"articleCategory": "filmai", "tagCategory": "kultūra"},
    {"articleCategory": "teatras", "tagCategory": "kultūra"},
    {"articleCategory": "muzika", "tagCategory": "kultūra"},
    {"articleCategory": "tautos", "tagCategory": "kultūra"},
    {"articleCategory": "kalba", "tagCategory": "kultūra"},
    {"articleCategory": "mada", "tagCategory": "kultūra"},
    {"articleCategory": "turizmas", "tagCategory": "kultūra"},
    {"articleCategory": "architektūra", "tagCategory": "kultūra"},
]


for category in categories:
    print(category["articleCategory"])
    getArticles(category["articleCategory"], category["tagCategory"], 4)

f.close()