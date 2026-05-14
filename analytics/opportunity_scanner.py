import pandas as pd

UNIVERSE = [
("NVDA","STOCK","US","Semiconductors","AI accelerator leader",86,72),
("AMD","STOCK","US","Semiconductors","AI chip competitor",82,64),
("MSFT","STOCK","US","Software","Cloud and AI platform",81,42),
("AVGO","STOCK","US","Semiconductors","AI networking and chips",79,58),
("QQQ","ETF","US","ETF","Nasdaq 100 growth",77,48),
("TEC","ETF","Canada","Technology","Canadian-listed global tech",75,50),
("VFV","ETF","Canada","ETF","S&P 500 CAD exposure",72,34),
("VEQT","ETF","Canada","ETF","Global diversification",70,28),
("COST","STOCK","US","Defensive","Quality compounder",68,30),
("SPY","ETF","US","ETF","US benchmark",66,35),
("JPM","STOCK","US","Financials","Large US bank",66,39),
("AAPL","STOCK","US","Technology","Consumer tech ecosystem",65,38),
("GOOGL","STOCK","US","Communication","Search, cloud, AI",64,41),
("AMZN","STOCK","US","Cloud/Consumer","AWS and commerce",64,45),
("META","STOCK","US","Communication","Ads and AI",63,50),
("ZGD","ETF","Canada","Materials","Gold miners hedge",62,61),
("V","STOCK","US","Payments","Global payments",61,31),
("MA","STOCK","US","Payments","Global payments",60,33),
("SHOP","STOCK","Canada","Software","Canadian growth tech",59,61),
("XIU","ETF","Canada","ETF","TSX 60",58,30),
("XIC","ETF","Canada","ETF","Canadian total market",57,30),
("RY","STOCK","Canada","Financials","Canadian bank",56,39),
("TD","STOCK","Canada","Financials","Canadian bank",55,45),
("ENB","STOCK","Canada","Energy","Pipeline income",54,43),
("CNQ","STOCK","Canada","Energy","Energy producer",54,55),
("BAM","STOCK","Canada","Asset Mgmt","Alternative assets",53,47),
]

def score_universe():
    df = pd.DataFrame(UNIVERSE, columns=["ticker","asset_type","country","sector","theme","opportunity_score","risk_score"])
    df["momentum_score"] = (df["opportunity_score"] - 3).clip(0,100)
    df["liquidity_score"] = (100 - df["risk_score"]).clip(0,100)
    df["macro_score"] = (df["opportunity_score"] - 5).clip(0,100)
    df["news_score"] = (df["opportunity_score"] - df["risk_score"]/3).clip(0,100)
    df["fundamental_score"] = (df["opportunity_score"] - 10).clip(0,100)
    df["action"] = ["candidate" if o >= 80 and r <= 65 else "watch" for o, r in zip(df.opportunity_score, df.risk_score)]
    df["reason"] = df["theme"] + ". MVP score; replace with live data in Phase 2."
    return df.sort_values("opportunity_score", ascending=False)
