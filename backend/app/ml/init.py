from joblib import load
from .features import vector
MODEL=load('app/ml/model.joblib')
def risk(url,meta):return round(MODEL.predict_proba([vector(url,meta)])[0][1]*100,2)
