import pandas as pd, glob, json, os
from utils import log_setup, ensure_dirs

def infer(df):
    return [{"field":c, "dtype":str(df[c].dtype), "non_null":int(df[c].notna().sum())} for c in df.columns]

def main():
    log_setup(); ensure_dirs()
    lines=["# Data Dictionary\n"]
    for path in sorted(glob.glob("data/clean/*.csv")):
        name=os.path.basename(path)
        df=pd.read_csv(path, nrows=1000)
        lines.append(f"## {name}\n")
        lines.append("| field | dtype | non_null | description |\n|---|---|---|---|\n")
        for row in infer(df):
            lines.append(f"| {row['field']} | {row['dtype']} | {row['non_null']} |  |\n")
    with open("docs/data_dictionary.md","w") as f: f.writelines(lines)
if __name__=="__main__": main()
