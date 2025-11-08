import os
import logging
import shutil
import pandas as pd
from utils import log_setup, ensure_dirs, safe_write_csv
import kagglehub

def main():
    """
    Download the Olist Brazilian E-commerce dataset from Kaggle and save to data/raw/.
    Returns a dictionary of DataFrames, one for each CSV file in the dataset.
    """
    try:
        log_setup()
        ensure_dirs()
        
        # Create raw directory if it doesn't exist
        raw_dir = "data/raw"
        os.makedirs(raw_dir, exist_ok=True)
        
        logging.info("Downloading Olist Brazilian E-commerce dataset from Kaggle...")
        dataset_path = kagglehub.dataset_download("olistbr/brazilian-ecommerce")
        
        # List all CSV files in the dataset directory
        csv_files = [f for f in os.listdir(dataset_path) if f.endswith('.csv')]
        
        if not csv_files:
            raise FileNotFoundError("No CSV files found in the downloaded dataset")
        
        # Load each CSV, save to data/raw/, and store in dictionary
        data_frames = {}
        for csv_file in csv_files:
            name = os.path.splitext(csv_file)[0]
            src_path = os.path.join(dataset_path, csv_file)
            dest_path = os.path.join(raw_dir, csv_file)
            
            # Read the CSV
            df = pd.read_csv(src_path)
            data_frames[name] = df
            
            # Save to data/raw/
            safe_write_csv(df, dest_path)
            logging.info(f"Saved {csv_file} to {dest_path} with shape {df.shape}")
        
        logging.info(f"\nSuccessfully downloaded and saved {len(data_frames)} tables to {raw_dir}/")
        logging.info("Available tables: " + ", ".join(data_frames.keys()))
        
        return data_frames
        
    except Exception as e:
        logging.error(f"Error in get_olist: {str(e)}")
        raise

def clean_olist():
    """Clean the Olist dataset and save to data/clean/"""
    try:
        from clean_structured import main as clean_structured
        clean_structured()
    except Exception as e:
        logging.error(f"Error cleaning Olist data: {str(e)}")
        raise

if __name__ == "__main__":
    # Download and save the data
    data = main()
    
    # Clean the data
    clean_olist()
    
    # Print sample output
    if data:
        first_table = next(iter(data.values()))
        print("\nFirst few rows of the first table:")
        print(first_table.head())
