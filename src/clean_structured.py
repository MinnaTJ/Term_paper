import pandas as pd, glob, logging
from utils import log_setup, ensure_dirs, safe_write_csv

def basic_clean(df):
    # standardize colnames
    df.columns = [c.strip().lower().replace(" ","_") for c in df.columns]
    # trim whitespace
    df = df.applymap(lambda x: x.strip() if isinstance(x,str) else x)
    return df

def main():
    log_setup(); ensure_dirs()
    for path in glob.glob("data/raw/olist_*.csv"):
        df=pd.read_csv(path, low_memory=False)
        df=basic_clean(df)
        out=path.replace("data/raw","data/clean")
        safe_write_csv(df,out)
        logging.info(f"cleaned_structured | in={path} out={out} rows={len(df)}")
if __name__=="__main__": main()
