import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("lemmatized.csv")


df["content"] = df["content"].fillna("")

X_train, X_test, y_train, y_test = train_test_split(df["content"], df["category"], test_size=0.2, random_state=42, stratify=df["category"])

vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1,2))
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

model = LogisticRegression(max_iter=2000, solver="saga", C=0.1, n_jobs=-1)
model.fit(X_train_tfidf, y_train)

y_pred = model.predict(X_test_tfidf)
report = classification_report(y_test, y_pred, output_dict=True)

plt.figure(figsize=(10, 6))
sns.heatmap(pd.DataFrame(report).iloc[:-1, :].T, annot=True, fmt=".2f", cm="Greens")
plt.title("Klasifikacijos tikslumo reportažas")
plt.tight_layout()
plt.savefig("classificationReport.png")
plt.show()

confusionMatrix = confusion_matrix(y_test, y_pred, labels=model.classes_)
confusionMatrixDisplay = ConfusionMatrixDisplay(confusion_matrix=confusionMatrix, display_labels=model.classes_)
confusionMatrixDisplay.plot(xticks_rotation="vertical", confusionMatrixap="Greens")
plt.title("Paivianos Matrica")
plt.tight_layout()
plt.savefig("confusionMatrix.png")
plt.show()
