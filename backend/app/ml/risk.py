"""
Combina a probabilidade do Random-Forest com um ajuste heurístico.

score_final = clamp( 100·prob_rf + Σ(pesos_positivos) )
onde cada flag crítica acrescenta (ou retira) pontos.
"""

from pathlib import Path
import numpy as np
import joblib

# ────────────── carregar modelo treinado ──────────────
MODEL_PATH = Path(__file__).with_suffix("") / "model.joblib"
_RF = joblib.load(MODEL_PATH)        # RandomForestClassifier

# ────────────── vetor de features usadas no treino ──────────────
def _vector(meta: dict) -> np.ndarray:
    return np.array([
        int(meta.get("dynamic_dns", 0)),
        int(meta.get("brand_similar", 0)),
        meta.get("hops", 0),
    ]).reshape(1, -1)

# ────────────── pesos heurísticos ──────────────
WEIGHTS = {
    "blacklist":            40,   # PhishTank
    "patterns":             15,
    "young_domain":         15,
    "ssl_expired":          10,
    "ssl_cn_mismatch":      10,
    "dynamic_dns":          10,
    "brand_similar":        10,
    "redirect_suspicious":   5,
    # popular_domain diminui risco – só adiciona se False
    "popular_domain":       25,
}

def _heuristic_boost(meta: dict) -> int:
    boost = 0
    for k, w in WEIGHTS.items():
        if k == "popular_domain":
            # soma w apenas se NÃO for popular
            if not meta.get("popular_domain"):
                boost += w
        elif meta.get(k):
            boost += w
    return boost

# ────────────── API pública ──────────────
def risk(url: str, meta: dict) -> int:
    """
    Calcula score 0–100 combinando
      • probabilidade do Random-Forest
      • boost heurístico baseado em flags críticas
    """
    prob = float(_RF.predict_proba(_vector(meta))[0, 1])   # 0–1
    base = prob * 100
    score = round(base + _heuristic_boost(meta))
    return max(0, min(score, 100))
