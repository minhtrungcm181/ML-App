import pickle

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree

df = pd.read_csv("data_training.csv")

print(df.head())

X = df[["Voltage", "Current", "TruePower", "ApparentPower"]]
y = df["Class"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=100)

clf_entropy = DecisionTreeClassifier(criterion="entropy", random_state=100, max_depth=3, min_samples_leaf=5)
clf_entropy.fit(X_train, y_train)

y_pred_en = clf_entropy.predict(X_test)
print(y_pred_en)

print("Accuracy is", accuracy_score(y_test,y_pred_en)*100)

pickle.dump(clf_entropy, open("modelA.pkl", "wb"))