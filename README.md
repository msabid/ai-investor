# AI Portfolio Command Center — Phase 1.5

Secure online-ready dashboard with:

- Login
- Dropdown/grouped navigation
- Dark/light theme
- Editable risk settings
- Expanded opportunity scanner
- AI recommendations
- Agent paper execution
- Future-ready live execution pathway

## Important

Agent execution is enabled now for **paper/simulated execution only**.

Real trading is not active, but the architecture keeps the future pathway open through:

- `ExecutionMode`
- `BrokerInterface`
- `PaperBroker`
- `LiveBrokerPlaceholder`
- `ExecutionController`
- risk gate
- human approval gate
- kill-switch gate

## Run

```bash
cd ai-portfolio-command-center-phase-1-5
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Default login:

- Email: `admin@example.com`
- Password: `ChangeMeNow123!`

Change before deployment.


## Auth Redesign Update

Added:
- Centered product-style login/register screen
- Registration tab
- Password strength validation
- Change-password page
- Improved dark styling and alignment
