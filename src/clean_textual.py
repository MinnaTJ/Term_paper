import pandas as pd
from langdetect import detect
from utils import load_cfg, ensure_dirs, log_setup, safe_write_csv
import logging
import glob
import os
import sys
from pathlib import Path

# Add src directory to path to allow importing from utils
sys.path.append(str(Path(__file__).parent))

def is_lang(s, allowed):
    """Check if text is in allowed languages."""
    try:
        return detect(str(s) or "") in allowed
    except Exception as e:
        logging.warning(f"Language detection failed: {e}")
        return False

def process_file(path, kind, cfg):
    """Process a single file based on its kind (news, tweets, etc.)."""
    try:
        logging.info(f"Processing {kind} file: {path}")
        df = pd.read_csv(path)
        
        if df.empty:
            logging.warning(f"Empty DataFrame in {path}")
            return df
            
        # Log initial stats
        initial_rows = len(df)
        logging.info(f"Initial rows: {initial_rows}")
        
        # Ensure text column exists and has content
        if "text" not in df.columns or df["text"].fillna('').str.strip().eq('').all():
            logging.warning(f"No content in 'text' column in {path}, using 'summary' instead")
            df["text"] = df.get("summary", "")
            
            # If summary contains HTML, extract the link text
            if df["text"].str.contains('<a href=').any():
                logging.info("Extracting text from HTML links in summary")
                df["text"] = df["text"].str.extract(r'<a[^>]*>(.*?)</a>', expand=False).fillna('')
        
        # Clean and filter data
        df["text"] = df["text"].fillna("").astype(str)
        
        # Filter by minimum text length
        # Use a lower threshold for news since the extracted text is often short
        min_len = 50 if kind == "news" else cfg["cleaning"].get("min_tweet_len", 20)
        df = df[df["text"].str.len() >= min_len]
        logging.info(f"After length filter (min {min_len} chars): {len(df)} rows")
        
        # Drop duplicates
        if kind == "news":
            drop_cols = [col for col in ["url", "title", "text"] if col in df.columns]
        else:  # tweets
            drop_cols = [col for col in ["tweet_id", "text", "url"] if col in df.columns]
            
        if drop_cols:
            initial_count = len(df)
            df = df.drop_duplicates(subset=drop_cols, keep="first")
            dropped = initial_count - len(df)
            if dropped > 0:
                logging.info(f"Dropped {dropped} duplicate rows")
        
        # Filter by language
        if "lang" in cfg and kind == "news":  # Only filter news by language
            initial_count = len(df)
            df = df[df["text"].apply(lambda x: is_lang(x, cfg["lang"]))]
            dropped = initial_count - len(df)
            if dropped > 0:
                logging.info(f"Dropped {dropped} rows not matching language {cfg['lang']}")
        
        # Select relevant columns
        if kind == "news":
            desired_cols = ["published_at", "title", "summary", "text", "url", "source", "category"]
        else:  # tweets
            desired_cols = ["created_at", "username", "displayname", "text", 
                          "like_count", "retweet_count", "reply_count", "url", "tweet_id"]
        
        keep = [col for col in desired_cols if col in df.columns]
        if not keep:
            logging.warning(f"No desired columns found in {path}")
            return pd.DataFrame()
            
        return df[keep]
        
    except Exception as e:
        logging.error(f"Error processing {path}: {str(e)}", exc_info=True)
        return pd.DataFrame()

def main():
    """Main function to clean all text data."""
    try:
        log_setup()
        ensure_dirs()
        cfg = load_cfg()
        
        # Create clean directory if it doesn't exist
        os.makedirs("data/clean", exist_ok=True)
        
        # Process news files
        news_files = glob.glob("data/raw/ecommerce_news_*.csv")
        if not news_files:
            logging.warning("No news files found in data/raw/")
        
        for path in news_files:
            try:
                out = path.replace("data/raw", "data/clean")
                logging.info(f"\nProcessing news file: {path}")
                df = process_file(path, "news", cfg)
                if not df.empty:
                    safe_write_csv(df, out)
                    logging.info(f"✅ Cleaned news | in={path} out={out} rows={len(df)}")
                else:
                    logging.warning(f"⚠️  No valid rows after cleaning: {path}")
            except Exception as e:
                logging.error(f"❌ Failed to process {path}: {str(e)}", exc_info=True)
        
        # Process tweet files (if any)
        tweet_files = glob.glob("data/raw/ecommerce_tweets_*.csv")
        if tweet_files:
            for path in tweet_files:
                try:
                    out = path.replace("data/raw", "data/clean")
                    logging.info(f"\nProcessing tweet file: {path}")
                    df = process_file(path, "tweets", cfg)
                    if not df.empty:
                        safe_write_csv(df, out)
                        logging.info(f"✅ Cleaned tweets | in={path} out={out} rows={len(df)}")
                except Exception as e:
                    logging.error(f"❌ Failed to process {path}: {str(e)}", exc_info=True)
        else:
            logging.info("No tweet files found in data/raw/")
        
        # Process complaint files (if any)
        complaint_files = glob.glob("data/raw/complaints_*.csv")
        if complaint_files:
            for path in complaint_files:
                try:
                    out = path.replace("data/raw", "data/clean")
                    logging.info(f"\nProcessing complaint file: {path}")
                    df = pd.read_csv(path)
                    initial_count = len(df)
                    
                    # Drop duplicates
                    drop_cols = [col for col in ["url", "title", "text"] if col in df.columns]
                    if drop_cols:
                        df = df.drop_duplicates(subset=drop_cols, keep="first")
                        dropped = initial_count - len(df)
                        if dropped > 0:
                            logging.info(f"Dropped {dropped} duplicate complaints")
                    
                    safe_write_csv(df, out)
                    logging.info(f"✅ Cleaned complaints | in={path} out={out} rows={len(df)}")
                except Exception as e:
                    logging.error(f"❌ Failed to process {path}: {str(e)}", exc_info=True)
        else:
            logging.info("No complaint files found in data/raw/")
            
    except Exception as e:
        logging.critical(f"❌ Fatal error in clean_textual.py: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
