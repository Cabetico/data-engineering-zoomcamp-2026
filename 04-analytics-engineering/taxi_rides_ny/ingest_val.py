import duckdb
import requests
from pathlib import Path

BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download"

def validate_parquet(filepath):
    """Check if parquet file is valid"""
    try:
        con = duckdb.connect()
        con.execute(f"SELECT COUNT(*) FROM read_parquet('{filepath}')")
        con.close()
        return True
    except Exception as e:
        print(f"Invalid parquet file {filepath}: {e}")
        return False

def download_and_convert_files(taxi_type):
    data_dir = Path("data") / taxi_type
    data_dir.mkdir(exist_ok=True, parents=True)

    for year in [2019, 2020]:
        for month in range(1, 13):
            parquet_filename = f"{taxi_type}_tripdata_{year}-{month:02d}.parquet"
            parquet_filepath = data_dir / parquet_filename

            # Check if file exists AND is valid
            if parquet_filepath.exists():
                if validate_parquet(parquet_filepath):
                    print(f"Skipping {parquet_filename} (already exists and valid)")
                    continue
                else:
                    print(f"Removing corrupted file {parquet_filename}")
                    parquet_filepath.unlink()

            # Download CSV.gz file
            csv_gz_filename = f"{taxi_type}_tripdata_{year}-{month:02d}.csv.gz"
            csv_gz_filepath = data_dir / csv_gz_filename

            try:
                print(f"Downloading {csv_gz_filename}...")
                response = requests.get(f"{BASE_URL}/{taxi_type}/{csv_gz_filename}", stream=True)
                response.raise_for_status()

                with open(csv_gz_filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                print(f"Converting {csv_gz_filename} to Parquet...")
                con = duckdb.connect()
                
                # Try with more lenient CSV parsing options
                con.execute(f"""
                    COPY (
                        SELECT * FROM read_csv_auto(
                            '{csv_gz_filepath}',
                            ignore_errors=true,
                            sample_size=-1
                        )
                    )
                    TO '{parquet_filepath}' (FORMAT PARQUET)
                """)
                con.close()

                # Validate the converted file
                if not validate_parquet(parquet_filepath):
                    print(f"ERROR: Failed to create valid parquet file {parquet_filename}")
                    if csv_gz_filepath.exists():
                        csv_gz_filepath.unlink()
                    if parquet_filepath.exists():
                        parquet_filepath.unlink()
                    continue

                # Remove the CSV.gz file to save space
                csv_gz_filepath.unlink()
                print(f"Completed {parquet_filename}")
                
            except requests.exceptions.HTTPError as e:
                print(f"Failed to download {csv_gz_filename}: {e}")
                # Clean up any partial files
                if csv_gz_filepath.exists():
                    csv_gz_filepath.unlink()
                continue
                
            except Exception as e:
                print(f"Error processing {csv_gz_filename}: {e}")
                # Clean up any partial files
                if csv_gz_filepath.exists():
                    csv_gz_filepath.unlink()
                if parquet_filepath.exists():
                    parquet_filepath.unlink()
                continue

def update_gitignore():
    gitignore_path = Path(".gitignore")

    # Read existing content or start with empty string
    content = gitignore_path.read_text() if gitignore_path.exists() else ""

    # Add data/ if not already present
    if 'data/' not in content:
        with open(gitignore_path, 'a') as f:
            f.write('\n# Data directory\ndata/\n' if content else '# Data directory\ndata/\n')

if __name__ == "__main__":
    # Update .gitignore to exclude data directory
    update_gitignore()

    for taxi_type in ["yellow", "green", "fhv"]:
        print(f"\n{'='*60}")
        print(f"Processing {taxi_type} data")
        print(f"{'='*60}")
        download_and_convert_files(taxi_type)

    print("\n" + "="*60)
    print("Creating DuckDB tables...")
    print("="*60)
    
    con = duckdb.connect("taxi_rides_ny.duckdb")
    con.execute("CREATE SCHEMA IF NOT EXISTS prod")

    for taxi_type in ["yellow", "green", "fhv"]:
        try:
            # Check if any parquet files exist
            parquet_files = list(Path(f"data/{taxi_type}").glob("*.parquet"))
            if not parquet_files:
                print(f"No parquet files found for {taxi_type}, skipping...")
                continue
                
            con.execute(f"""
                CREATE OR REPLACE TABLE prod.{taxi_type}_tripdata AS
                SELECT * FROM read_parquet('data/{taxi_type}/*.parquet', union_by_name=true)
            """)
            
            # Get row count
            count = con.execute(f"SELECT COUNT(*) FROM prod.{taxi_type}_tripdata").fetchone()[0]
            print(f"✓ Created table prod.{taxi_type}_tripdata with {count:,} rows")
            
        except Exception as e:
            print(f"✗ ERROR creating table for {taxi_type}: {e}")

    con.close()
    print("\n" + "="*60)
    print("Done!")
    print("="*60)