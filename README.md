# AI Portfolio Command Center

A Python-based AI-assisted investing and trading platform for a Canadian investor.

## Primary Rule

1. Survival and capital preservation  
2. Long-term compounding  
3. Maximizing returns  

This system never promises guaranteed profits. It starts with dashboard, tracking, paper trading, and strict risk controls before any broker execution.

## MVP Includes

- Streamlit dashboard shell
- SQLite schema
- Manual holdings input
- Portfolio value chart
- Basic market data module
- Basic risk status display
- Agent logging
- QA checklist shell
- No real trading

## Install

```bash
cd ai-portfolio-command-center
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
# .venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

## Safety Defaults

- Live trading disabled
- Paper trading disabled
- Margin disabled
- TFSA treated as long-term investing only
- No options
- No naked derivatives
- No automated execution
