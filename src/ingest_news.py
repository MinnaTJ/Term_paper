import pandas as pd, requests, time
from bs4 import BeautifulSoup
from dateutil import parser
from utils import load_cfg, ensure_dirs, log_setup, month_range, safe_write_csv, normalize_text
import logging, re

def fetch_feed(url):
    try:
        r = requests.get(url, timeout=20)
        soup = BeautifulSoup(r.text, "xml")
        items=[]
        for it in soup.find_all("item"):
            title = it.title.text if it.title else ""
            link  = it.link.text if it.link else ""
            pub   = it.pubDate.text if it.pubDate else ""
            ts    = parser.parse(pub).isoformat() if pub else None
            desc  = it.description.text if it.description else ""
            items.append(dict(title=title, url=link, published_at=ts, summary=desc, source=url))
        return pd.DataFrame(items)
    except Exception as e:
        logging.exception(f"feed_error: {url} -> {e}")
        return pd.DataFrame([])

def main():
    log_setup(); cfg = load_cfg(); ensure_dirs()
    months = month_range(cfg["months_back"], cfg["timezone"])
    feeds  = cfg["news"]["rss_feeds"]
    all_df = pd.concat([fetch_feed(u) for u in feeds], ignore_index=True)
    # basic content fetch for full text where possible
    texts=[]
    for _,row in all_df.iterrows():
        txt=""
        try:
            r=requests.get(row["url"], timeout=15)
            soup=BeautifulSoup(r.text, "html.parser")
            # naive text grab
            paras=[p.get_text(" ", strip=True) for p in soup.find_all("p")]
            txt=" ".join(paras)
        except: pass
        texts.append(txt)
    all_df["text"]= [normalize_text(t) for t in texts]
    # month partition
    all_df["month"]= pd.to_datetime(all_df["published_at"], errors="coerce").dt.strftime("%Y%m")
    for m in months:
        dfm = all_df.query("month == @m")
        if dfm.empty: continue
        out=f"data/raw/ecommerce_news_{m}.csv"
        dfm = dfm.assign(category="news")
        safe_write_csv(dfm[["published_at","title","summary","text","url","source","category"]], out)
        logging.info(f"news | month={m} rows={len(dfm)} file={out}")
if __name__=="__main__": main()
