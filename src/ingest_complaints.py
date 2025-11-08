import pandas as pd, requests, logging, time
from bs4 import BeautifulSoup
from utils import load_cfg, ensure_dirs, log_setup, month_range, safe_write_csv

def scrape(url):
    try:
        r=requests.get(url, timeout=20, headers={"User-Agent":"Mozilla/5.0"})
        soup=BeautifulSoup(r.text,"html.parser")
        cards=soup.select("article, .complaint, .card, li")  # generic
        rows=[]
        for c in cards:
            title=c.get_text(" ", strip=True)[:200]
            rows.append({"title":title,"text":title,"url":url})
        return pd.DataFrame(rows)
    except Exception as e:
        logging.exception(f"complaints_error: {url} -> {e}")
        return pd.DataFrame()

def main():
    log_setup(); cfg=load_cfg(); ensure_dirs()
    urls=cfg["complaints"]["urls"]
    df=pd.concat([scrape(u) for u in urls], ignore_index=True) if urls else pd.DataFrame()
    if df.empty: return
    df["published_at"]=None; df["source"]="complaints_list"
    df["month"]="misc"
    out="data/raw/complaints_misc.csv"
    safe_write_csv(df[["published_at","title","text","url","source"]], out)
    logging.info(f"complaints | rows={len(df)} file={out}")
if __name__=="__main__": main()
