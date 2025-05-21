# PFTecHacker

# PhishGuard – Detector de Phishing (B-grade)
## Ferramenta open-source para análise de URLs e geração de score de risco (0-100) combinando heurísticas tradicionais + modelo de machine learning treinado em 30 k amostras.
## Interface web em Bulma + Chart.js com histórico local, download de relatório e captura de screenshot da página.

### Índice
* Demonstração rápida
* Funcionalidades
* Instalação
* Rodando a aplicação
* Estrutura de diretórios
* Datasets & treino de modelo
* Scripts utilitários
* Testes & CI
* Roadmap
* Licença

### Demonstração rápida
```bash
git clone https://github.com/<seu-user>/PhishGuard.git
cd PhishGuard
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.app.main:app --reload   # API + captura de screenshot
# em outro terminal
python -m http.server 9000 -d web       # UI estática
```

Abra `http://localhost:9000` – cole uma URL, clique Testar, visualize:

Score numérico + nível (baixo/médio/alto)

Flags heurísticas ✓ / ✗

Screenshot da página

Histograma de URLs analisadas

### Funcionalidades
Categoria	Implementação
Blacklists	CSV limpo do PhishTank (≈ 57 k URLs)
Whitelists	Top-1 M (Tranco) → flag “domínio conhecido”
Heurísticas	padrões suspeitos (números, subdomínios, chars), domínios Dyn-DNS, idade WHOIS < 180 d, SSL expirado / CN mismatch, redirecionamentos > 3 hops, similaridade de marca (Levenshtein)
Machine Learning	RandomForest (scikit-learn) treinado em 30 000 URLs (PhishTank × Top-10k Tranco) – features: comprimento, nº de subdomínios, caracteres especiais, idade WHOIS, hops, flags heurísticas
Score final	score = 0.6·ml_score + 0.4·penalty(flags) (pesos configuráveis em backend/app/ml/risk.py)
API	FastAPI /api/v2/score – body { "url": "<URL>" } – retorna JSON com score, flags, screenshot
Screenshot	Playwright → PNG salvo em media/shots/<hash>.png
Interface Web	Bulma + Chart.js; histórico em localStorage; modal detalhado; gráfico pizza Maliciosas × Seguras
CI	GitHub Actions executa lint + pytest -q

### Instalação
Pré-requisitos
Python ≥ 3.10

Node ≥ 18 (apenas se quiser rebuildar a UI)

Sistema Linux/macOS; Windows WSL2 testado.

Passos
```bash
git clone https://github.com/<seu-user>/PhishGuard.git
cd PhishGuard
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt         # FastAPI, Playwright, scikit-learn…
playwright install chromium             # 1ª vez: baixa navegador headless
```

### Rodando a aplicação
Processo	Comando
API (backend)	uvicorn backend.app.main:app --reload
UI (estática)	python -m http.server 9000 -d web ou servir pelo Nginx/Apache
Abrir	http://localhost:9000

### Estrutura de diretórios
```bash
PhishGuard/
├── backend/
│   ├── app/
│   │   ├── detectors/          # heurísticas independentes
│   │   ├── ml/                 # feature vector + risk.py + model.joblib
│   │   ├── screenshot.py       # captura via Playwright
│   │   └── main.py             # FastAPI
│   └── tests/                  # pytest
├── datasets/
│   ├── tranco_top1m.csv        # whitelist (~1 MB, 20  primeiros mil)
│   └── phishtank_clean.csv     # blacklist limpa (sem chaves)
├── media/shots/                # screenshots gerados
├── scripts/
│   ├── build_dataset.py        # gera train.csv
│   ├── sanitize_phishtank.py   # remove linhas suspeitas
│   └── train_model.py          # treina RandomForest
└── web/                        # front-end Bulma + JS
```

### Datasets & treino de modelo
```bash
# recriar dataset de treino (leva ~1 h para 30 000 URLs)
PYTHONPATH=. python scripts/build_dataset.py

# treinar modelo e salvar em backend/app/ml/model.joblib
PYTHONPATH=. python scripts/train_model.py
Treina RandomForest com validação 80/20; F1 ≈ 0,96 (amostra interna).
```

### Scripts utilitários
Script	Função
sanitize_phishtank.py	filtra colunas inúteis + remove tokens parecidos c/ chaves AWS
build_dataset.py	junta PhishTank + Tranco, roda heurísticas, produz train.csv
train_model.py	lê train.csv, extrai features e grava modelo

### Testes & CI
```bash
pytest -q backend/tests       # 100 % passing
CI GitHub Actions (.github/workflows/ci.yml) executa:

pip install -r requirements.txt

pytest -q

flake8 (linter)
```
---
Dados derivados de:

PhishTank © Cisco (Creative Commons – Attribution)

Tranco Top-1M © KU Leuven (research license)

---
# “Don’t trust a URL by its cover.” – PhishGuard 🛡️
