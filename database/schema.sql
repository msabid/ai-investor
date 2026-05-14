CREATE TABLE IF NOT EXISTS users (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 email TEXT NOT NULL UNIQUE,
 password_hash TEXT NOT NULL,
 role TEXT NOT NULL DEFAULT 'admin',
 is_active INTEGER NOT NULL DEFAULT 1,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 last_login_at TEXT
);

CREATE TABLE IF NOT EXISTS risk_settings (
 id INTEGER PRIMARY KEY CHECK (id = 1),
 max_risk_per_trade REAL NOT NULL DEFAULT 0.01,
 daily_loss_limit REAL NOT NULL DEFAULT 0.02,
 weekly_loss_limit REAL NOT NULL DEFAULT 0.05,
 monthly_drawdown_limit REAL NOT NULL DEFAULT 0.08,
 single_stock_concentration_limit REAL NOT NULL DEFAULT 0.20,
 sector_concentration_limit REAL NOT NULL DEFAULT 0.35,
 min_cash_reserve REAL NOT NULL DEFAULT 0.05,
 margin_enabled INTEGER NOT NULL DEFAULT 0,
 options_enabled INTEGER NOT NULL DEFAULT 0,
 live_trading_enabled INTEGER NOT NULL DEFAULT 0,
 paper_trading_enabled INTEGER NOT NULL DEFAULT 1,
 agent_execution_enabled INTEGER NOT NULL DEFAULT 1,
 human_approval_required INTEGER NOT NULL DEFAULT 1,
 execution_mode TEXT NOT NULL DEFAULT 'PAPER',
 updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS proposed_trades (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 ticker TEXT NOT NULL,
 action TEXT NOT NULL,
 account_type TEXT NOT NULL,
 quantity REAL,
 estimated_price REAL,
 estimated_value REAL,
 max_loss REAL,
 stop_loss REAL,
 reason TEXT,
 risk_level TEXT,
 confidence_score REAL,
 status TEXT NOT NULL DEFAULT 'PROPOSED',
 execution_mode TEXT NOT NULL DEFAULT 'PAPER',
 human_approval_required INTEGER NOT NULL DEFAULT 1,
 approved INTEGER NOT NULL DEFAULT 0,
 created_by_agent TEXT,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS executed_trades (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 proposed_trade_id INTEGER,
 ticker TEXT NOT NULL,
 action TEXT NOT NULL,
 account_type TEXT NOT NULL,
 quantity REAL NOT NULL,
 fill_price REAL NOT NULL,
 fees REAL DEFAULT 0,
 slippage REAL DEFAULT 0,
 currency TEXT NOT NULL,
 execution_mode TEXT NOT NULL,
 broker TEXT NOT NULL,
 execution_status TEXT NOT NULL DEFAULT 'FILLED',
 executed_by TEXT NOT NULL DEFAULT 'ExecutionController',
 executed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS system_health (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 component TEXT NOT NULL,
 status TEXT NOT NULL,
 last_run TEXT,
 message TEXT,
 checked_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS agent_logs (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 agent_name TEXT NOT NULL,
 level TEXT NOT NULL,
 message TEXT NOT NULL,
 metadata TEXT,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
