import logging, os, sys, time
from datetime import datetime
from dateutil.relativedelta import relativedelta
import yaml, pandas as pd

def load_cfg(p="src/config.yaml"):
    with open(p) as f: return yaml.safe_load(f)

def ensure_dirs():
    for d in ["data/raw","data/clean","logs","docs","src"]:
        os.makedirs(d, exist_ok=True)

def log_setup():
    ensure_dirs()
    logging.basicConfig(
        filename="logs/ingestion.log",
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter("%(levelname)s | %(message)s"))
    logging.getLogger().addHandler(console)

def month_range(months_back, tz="Asia/Kolkata"):
    end = datetime.now()
    start = end - relativedelta(months=months_back-1)
    cur = datetime(start.year, start.month, 1)
    out=[]
    while cur <= end:
        out.append(cur.strftime("%Y%m"))
        cur += relativedelta(months=1)
    return out

def safe_write_csv(df, path):
    df.to_csv(path, index=False, encoding="utf-8")

def normalize_text(s):
    if not isinstance(s, str): return ""
    return " ".join(s.replace("\u00a0"," ").split())
