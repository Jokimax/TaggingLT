import csv
import os
from lemmatization import lemmatize

csv.field_size_limit(50000000)
texts = open("texts.csv", "r", encoding="utf-8")
data = csv.DictReader(texts)

fileExists = os.path.exists("lemmatized.csv")
f = open("lemmatized.csv", "a", encoding="utf-8")

writer = csv.DictWriter(f, fieldnames=["content", "category"])
if(not fileExists): writer.writeheader()
for text in data:
    lemmatizedText = lemmatize(text["content"])
    writer.writerow({"content": lemmatizedText, "category": text["category"]})
f.close()
texts.close()
