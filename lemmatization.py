import stanza
import re

cleanRegex = re.compile(r'[^a-ząčęėįšųūž ]')
emptyCleanRegex = re.compile(r'\s+')

try:
    nlp = stanza.Pipeline('lt', processors='tokenize,lemma', download_method = None)
except stanza.models.common.UnknownLanguageError:
    stanza.download('lt')
    nlp = stanza.Pipeline('lt', processors='tokenize,lemma')

f = open("stopwords.txt", "r", encoding="utf-8")
wordsToIgnore = set(f.readline().split())
f.close()

def lemmatize(text):
    text = text.lower()
    text = re.sub(cleanRegex, '', text)
    text = re.sub(emptyCleanRegex, ' ', text)

    doc = nlp(text)

    lemmatizedText = ""

    for sentence in doc.sentences:
        for word in sentence.words:
            if(not word.lemma in  wordsToIgnore):
                lemmatizedText += word.lemma + " "
    return lemmatizedText