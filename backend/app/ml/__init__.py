from joblib import load
from pathlib import Path
from .features import vector
# carrega modelo (use o caminho correto)
MODEL_PATH = Path(__file__).with_suffix('').parent / 'model.joblib'
MODEL = load(MODEL_PATH)
def risk(url, meta):
 return round(MODEL.predict_proba([vector(url, meta)])[0][1] * 100, 2)
