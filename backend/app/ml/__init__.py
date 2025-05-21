# backend/app/ml/__init__.py
from pathlib import Path
from joblib import load
from .features import vector

MODEL_PATH = Path(__file__).resolve().parent / "model.joblib"
_MODEL = None

def _ensure_loaded():
    global _MODEL
    if _MODEL is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError("model.joblib inexistente – rode train.py primeiro")
        _MODEL = load(MODEL_PATH)

def risk(url: str, meta: dict) -> float:
    _ensure_loaded()
    prob = _MODEL.predict_proba([vector(url, meta)])[0][1]
    return round(prob * 100, 2)
