import pandas as pd, subprocess, json, logging
from utils import load_cfg, ensure_dirs, log_setup, month_range, safe_write_csv
from datetime import datetime
from dateutil.relativedelta import relativedelta

def daterange_for_month(ym):
    y=int(ym[:4]); m=int(ym[4:])
    start=datetime(y,m,1)
    end=(start + relativedelta(months=1))
    return start.date().isoformat(), end.date().isoformat()

def scrape_month(q, ym, limit):
    since, until = daterange_for_month(ym)
    cmd = f'snscrape --jsonl --max-results {limit} --since {since} twitter-search "{q} until:{until}"'
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    rows=[json.loads(l) for l in proc.stdout.splitlines() if l.strip()]
    if not rows: return pd.DataFrame()
    return pd.DataFrame([{
        "tweet_id": r.get("id"),
        "created_at": r.get("date"),
        "username": r.get("user",{}).get("username"),
        "displayname": r.get("user",{}).get("displayname"),
        "text": r.get("rawContent"),
        "like_count": r.get("likeCount"),
        "retweet_count": r.get("retweetCount"),
        "reply_count": r.get("replyCount"),
        "url": r.get("url")
    } for r in rows])

def main():
    log_setup(); cfg=load_cfg(); ensure_dirs()
    months = month_range(cfg["months_back"])
    q=cfg["tweets"]["query"]; limit=cfg["tweets"]["max_per_month"]
    for m in months:
        df=scrape_month(q, m, limit)
        if df.empty: continue
        out=f"data/raw/ecommerce_tweets_{m}.csv"
        df.to_csv(out, index=False)
        logging.info(f"tweets | month={m} rows={len(df)} file={out}")
if __name__=="__main__": main()
