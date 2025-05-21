# backend/app/ml/train.py
from pathlib import Path
import pandas as pd, joblib
from sklearn.ensemble import RandomForestClassifier
from backend.app.ml.features import vector   # <– absoluto, sem “from .”

DATA = Path(__file__).resolve().parents[3] / "datasets" / "train.csv"
df = pd.read_csv(DATA)

X = [vector(r.url, r.to_dict()) for _, r in df.iterrows()]
y = df.label

clf = RandomForestClassifier(n_estimators=120, max_depth=9, random_state=42).fit(X, y)
out = Path(__file__).resolve().parent / "model.joblib"
joblib.dump(clf, out)
print("Modelo salvo em", out)
