# PFTecHacker

# PhishGuard – Detector de Phishing

## Ferramenta open-source para análise de URLs e geração de score de risco (0-100) combinando heurísticas tradicionais + modelo de machine learning treinado em 30k amostras.
Interface web com histórico local e captura de screenshot da página.

---

### Índice
* [Demonstração rápida](#demonstração-rápida)
* [Funcionalidades](#funcionalidades)
* [Instalação](#instalação)
* [Rodando a aplicação](#rodando-a-aplicação)
* [Estrutura de diretórios](#estrutura-de-diretórios)
* [Datasets & treino de modelo](#datasets--treino-de-modelo)
* [Scripts utilitários](#scripts-utilitários)
* [Créditos e Licença](#créditos-e-licença)

---

### Demonstração rápida

```bash
git clone https://github.com/Fdemaiaar/PFTecHacker.git
cd PFTecHacker
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.app.main:app --reload   # API + captura de screenshot
# em outro terminal
python -m http.server 9000 -d web       # UI estática
```

Acesse `http://localhost:9000` – cole uma URL, clique Testar e visualize:

- Score numérico + nível (baixo / médio / alto)
- Flags heurísticas ✓ / ✗
- Screenshot da página
- Histograma de URLs analisadas

---

### Funcionalidades

| Categoria     | Implementação |
|---------------|---------------|
| Blacklists    | CSV limpo do PhishTank (≈ 57k URLs) |
| Whitelists    | Top-1M (Tranco) → flag “domínio conhecido” |
| Heurísticas   | Padrões suspeitos (números, subdomínios, chars), domínios Dyn-DNS, idade WHOIS < 180d, SSL expirado / CN mismatch, redirecionamentos > 3 hops, similaridade de marca (Levenshtein) |
| Machine Learning | RandomForest (scikit-learn), 30k URLs – features: comprimento, nº subdomínios, chars especiais, idade WHOIS, hops, flags heurísticas |
| Score final   | score = 0.6·ml_score + 0.4·penalty(flags) – pesos ajustáveis (backend/app/ml/risk.py) |
| API           | FastAPI `POST /api/v2/score` → `{ "url": "<URL>" }` → JSON com score, flags, screenshot |
| Screenshot    | Playwright → PNG salvo em media/shots/<hash>.png |
| Interface Web | Bulma + Chart.js; histórico em localStorage; modal detalhado; pizza Maliciosas × Seguras |

---

### Instalação

**Pré-requisitos**

- Python ≥ 3.10
- Node ≥ 18 (apenas se quiser rebuildar a UI)
- Linux/macOS ou Windows com WSL2 testado

**Passos**

```bash
git clone https://github.com/Fdemaiaar/PFTecHacker.git
cd PhishGuard
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt         # FastAPI, Playwright, scikit-learn…
playwright install chromium             # 1ª vez: baixa navegador headless
```

---

### Rodando a aplicação

| Processo     | Comando |
|--------------|---------|
| API (backend) | uvicorn backend.app.main:app --reload |
| UI (estática) | python -m http.server 9000 -d web ou servir via Nginx/Apache |
| Abrir        | http://localhost:9000 |

---

### Estrutura de diretórios

```txt
PhishGuard/
├── backend/
│   ├── app/
│   │   ├── detectors/          # heurísticas independentes
│   │   ├── ml/                 # feature vector + risk.py + model.joblib
│   │   ├── screenshot.py       # captura via Playwright
│   │   └── main.py             # FastAPI
│   └── tests/                  # pytest
├── datasets/
│   ├── tranco_top1m.csv        # whitelist (~1 MB, 20k primeiros)
│   └── phishtank_clean.csv     # blacklist limpa (sem chaves)
├── media/shots/                # screenshots gerados
├── scripts/
│   ├── build_dataset.py        # gera train.csv
│   ├── sanitize_phishtank.py   # remove linhas suspeitas
│   └── train_model.py          # treina RandomForest
└── web/                        # front-end Bulma + JS
```

---

### Datasets & treino de modelo

```bash
# recriar dataset de treino (leva ~14h para 30k URLs)
PYTHONPATH=. python scripts/build_dataset.py

# treinar modelo e salvar em backend/app/ml/model.joblib
PYTHONPATH=. python scripts/train_model.py
```

Treinamento com validação 80/20. F1-score interno: ≈ 0.96

---

### Scripts utilitários

| Script                | Função |
|------------------------|--------|
| sanitize_phishtank.py | filtra colunas + remove tokens tipo chaves AWS |
| build_dataset.py      | junta PhishTank + Tranco, roda heurísticas, gera train.csv |
| train_model.py        | extrai features e salva modelo RandomForest |

---

### Créditos e Licença

- Dados derivados de:
  - PhishTank © Cisco (Creative Commons – Attribution)
  - Tranco Top-1M © KU Leuven (research license)

---

# “Don’t trust a URL by its cover.” – PhishGuard 🛡️
