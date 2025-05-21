import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import csv

prevDocuments = set()

f = open("lrs.csv", "w", encoding="utf-8")
writer = csv.DictWriter(f, fieldnames=["content", "category"])
writer.writeheader()

def removePrefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

def getLegalDocument(oid):
    url = "https://e-seimas.lrs.lt/rs/legalact/TAP/" + oid

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    body = soup.body
    if(body == None): return None
    legalDocument = body.get_text(separator=" ", strip=True)
    legalDocument = removePrefix(legalDocument, "Projektas ")
    return legalDocument.strip().replace("\n","")

for id in range(-502065, -500010):
    url = "https://apps.lrs.lt/sip/p2b.ad_sp_darbotvarke?posedzio_id=" + str(id)
    response = requests.get(url)
    root = ET.fromstring(response.content)

    if(root.find(".//SeimoPosėdis") == None): continue

    for session in root.find(".//SeimoPosėdis").findall(".//DarbotvarkėsKlausimas"):
        if(session.find(".//KlausimoStadija") == None or session.find(".//KlausimoStadija").attrib.get("dokumento_nuoroda") == None): continue
        document = session.find(".//KlausimoStadija").attrib.get("dokumento_nuoroda")
        oid = document.rsplit('/', 1)[-1]

        if(oid == None or oid in prevDocuments): continue
        prevDocuments.add(oid)

        legalDocument = getLegalDocument(oid)
        if(legalDocument == None): continue
        writer.writerow({"content": legalDocument, "category": "politika"})

f.close()