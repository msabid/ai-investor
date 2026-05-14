import json
from datetime import datetime
from database.db import run_query

class BaseAgent:
    def __init__(self, name):
        self.name = name

    def log(self, level, message, metadata=None):
        run_query(
            "INSERT INTO agent_logs(agent_name,level,message,metadata) VALUES(:a,:l,:m,:d)",
            {"a": self.name, "l": level, "m": message, "d": json.dumps(metadata or {})}
        )

    def health(self, status, message):
        run_query(
            "INSERT INTO system_health(component,status,last_run,message) VALUES(:c,:s,:r,:m)",
            {"c": self.name, "s": status, "r": datetime.utcnow().isoformat(), "m": message}
        )
