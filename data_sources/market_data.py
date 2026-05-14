import random
from datetime import datetime

PRICES = {
"VFV":150,"VEQT":42,"ZGD":22,"NVDA":950,"AMD":160,"MSFT":420,"AAPL":190,
"GOOGL":170,"AMZN":185,"META":500,"AVGO":1400,"TSLA":180,"COST":820,
"JPM":200,"V":275,"MA":460,"SHOP":95,"RY":140,"TD":82,"ENB":50,
"CNQ":48,"BAM":55,"SPY":530,"QQQ":455,"XIU":34,"XIC":36,"TEC":35
}
CAD = {"VFV","VEQT","ZGD","SHOP","RY","TD","ENB","CNQ","BAM","XIU","XIC","TEC"}

class MarketDataClient:
    def get_price(self, ticker):
        t = ticker.upper().strip()
        base = PRICES.get(t, 100)
        return {
            "ticker": t,
            "price": round(base * random.uniform(.99, 1.01), 2),
            "currency": "CAD" if t in CAD else "USD",
            "source": "mock_phase_1_5",
            "timestamp": datetime.utcnow().isoformat()
        }
