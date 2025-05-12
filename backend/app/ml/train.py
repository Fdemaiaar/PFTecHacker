import pandas as pd, joblib
from sklearn.ensemble import RandomForestClassifier
from .features import vector
df = pd.read_csv('datasets/train.csv')  # colunas url,label + meta
X = [vector(row.url, row.to_dict()) for _, row in df.iterrows()]
y = df.label
clf = RandomForestClassifier(n_estimators=120, max_depth=9).fit(X, y)
joblib.dump(clf, 'backend/app/ml/model.joblib')
