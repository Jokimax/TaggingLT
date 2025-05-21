import numpy as np
import pickle
from lemmatization import lemmatize

f = open("logregModel.pkl", "rb")
model = pickle.load(f)
f.close()

f = open("vectorizer.pkl", "rb")
vectorizer = pickle.load(f)
f.close()

def tagText(text):
    text = lemmatize(text)
    textVector = vectorizer.transform([text])
    predicted_label = model.predict(textVector)
    return predicted_label[0]

lines = []
while True:
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break
    text = '\n'.join(lines)
    tag = tagText(text)

    print(f"Predicted Tag: {tag}")
    lines.clear()