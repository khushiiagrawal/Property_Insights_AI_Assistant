#!/usr/bin/env python3
"""
Index data into Qdrant from command line.

Usage:
    python index_data.py <file_path>
    
Example:
    python index_data.py property_transactions_dataset_clustered.csv
    python index_data.py data.json
"""

import sys
import pandas as pd
import time
from main import build_index_from_df, clear_and_rebuild_collection, qdrant
import config

def index_file(file_path):
    """Load and index a CSV or JSON file into Qdrant."""
    
    print(f"\n{'='*60}")
    print(f"📁 Loading dataset: {file_path}")
    print(f"{'='*60}\n")
    
    # Load the file
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.json'):
            df = pd.read_json(file_path)
        else:
            print("❌ Error: Unsupported file format. Use .csv or .json")
            return False
        
        print(f"✅ Loaded {len(df)} rows, {len(df.columns)} columns\n")
        
    except FileNotFoundError:
        print(f"❌ Error: File not found: {file_path}")
        return False
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return False
    
    # Clear old data
    print("🗑️  Clearing previous data from Qdrant...")
    clear_and_rebuild_collection()
    print("✅ Collection cleared\n")
    
    # Index data
    print(f"📊 Indexing {len(df)} rows into Qdrant...")
    build_index_from_df(df)
    print("✅ Successfully indexed\n")
    
    # Wait for indexing to complete
    print("⏳ Waiting for Qdrant to complete indexing...")
    time.sleep(2)
    
    # Verify
    collection_info = qdrant.get_collection(config.COLLECTION_NAME)
    
    print(f"\n{'='*60}")
    print("✨ SUCCESS!")
    print(f"{'='*60}")
    print(f"📈 Total documents indexed: {collection_info.points_count}")
    print(f"🗄️  Collection name: {config.COLLECTION_NAME}")
    print(f"🚀 Ready for queries!")
    print(f"\n💡 Start API with: python api.py")
    print(f"{'='*60}\n")
    
    return True

def main():
    if len(sys.argv) < 2:
        print("\n❌ Error: No file path provided")
        print("\nUsage:")
        print("  python index_data.py <file_path>")
        print("\nExample:")
        print("  python index_data.py property_transactions_dataset_clustered.csv")
        print("  python index_data.py data.json\n")
        sys.exit(1)
    
    file_path = sys.argv[1]
    success = index_file(file_path)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()

