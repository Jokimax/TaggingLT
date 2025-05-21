import matplotlib.pyplot as plt
import pickle
import numpy as np
import os

f = open("logregModel.pkl", "rb")
model = pickle.load(f)
f.close()

f = open("vectorizer.pkl", "rb")
vectorizer = pickle.load(f)
f.close()

os.makedirs("wordImportanceGraphs", exist_ok=True)

words = np.array(vectorizer.get_feature_names_out())

for i, category in enumerate(model.classes_):
    coefs = model.coef_[i]
    topIndexes = np.argsort(coefs)[-10:]
    topWords = words[topIndexes]
    topWeights = coefs[topIndexes]

    plt.figure(figsize=(10, 6))
    plt.barh(topWords, topWeights, color="skyblue")
    plt.title(f"Svarbiausi žodžiai kategorijai: {category}")
    plt.tight_layout()
    plt.savefig(f"wordImportanceGraphs/{category}_mostImportantWords.png")
    plt.close()