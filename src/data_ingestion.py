import os
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.customer_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml
from google.cloud import storage

# Add this line - replace the existing client initialization
client = storage.Client(project="direct-byte-450314-k1")

logger = get_logger(__name__)


class DataIngestion:
    def __init__(self, config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_name = self.config["bucket_file_name"]
        self.train_test_ratio = self.config["train_ratio"]

        os.makedirs(RAW_DIR, exist_ok=True)
        logger.info(f"Data Ingestion started with {self.bucket_name} and file is {self.file_name}")

    def download_csv_from_gcp(self):
        try:
            print(f"🔄 Connecting to GCP...")
            print(f"   Bucket: {self.bucket_name}")
            print(f"   File: {self.file_name}")
            print(f"   Download to: {RAW_FILE_PATH}")
            
            client = storage.Client()
            print("✅ GCP client created")
            
            bucket = client.bucket(self.bucket_name)
            print("✅ Bucket accessed")
            
            blob = bucket.blob(self.file_name)
            print("✅ Blob object created")
            
            # Check if blob exists
            if not blob.exists():
                raise Exception(f"File '{self.file_name}' does not exist in bucket '{self.bucket_name}'")
            
            print(f"✅ File exists in bucket, size: {blob.size} bytes")
            
            blob.download_to_filename(RAW_FILE_PATH)
            print(f"✅ File downloaded successfully")
            
            # Verify download
            if os.path.exists(RAW_FILE_PATH):
                file_size = os.path.getsize(RAW_FILE_PATH)
                print(f"✅ Downloaded file verified: {file_size} bytes")
                logger.info(f"CSV file is successfully downloaded to {RAW_FILE_PATH}")
            else:
                raise Exception("Download completed but file not found locally")
                
        except Exception as e:
            print(f"❌ GCP Download Error: {e}")
            logger.error(f"Error while downloading the csv file: {e}")
            raise CustomException("Failed to download csv file", e)

    def split_data(self):
        try:
            logger.info("Starting the splitting process")
            print(f"RAW_FILE_PATH: {RAW_FILE_PATH}")
            print(f"TRAIN_FILE_PATH: {TRAIN_FILE_PATH}")
            print(f"TEST_FILE_PATH: {TEST_FILE_PATH}")
            
            if not os.path.exists(RAW_FILE_PATH):
                logger.error(f"Raw file not found at {RAW_FILE_PATH}")
                return
                
            data = pd.read_csv(RAW_FILE_PATH)
            print(f"Data shape: {data.shape}")
            
            train_data, test_data = train_test_split(data, test_size=1-self.train_test_ratio, random_state=42)
            
            os.makedirs(os.path.dirname(TRAIN_FILE_PATH), exist_ok=True)
            os.makedirs(os.path.dirname(TEST_FILE_PATH), exist_ok=True)
            
            train_data.to_csv(TRAIN_FILE_PATH, index=False)
            test_data.to_csv(TEST_FILE_PATH, index=False)
            
            if os.path.exists(TRAIN_FILE_PATH):
                logger.info(f"✅ Train file created: {TRAIN_FILE_PATH}")
                print(f"Train file size: {os.path.getsize(TRAIN_FILE_PATH)} bytes")
            else:
                logger.error(f"❌ Train file NOT created: {TRAIN_FILE_PATH}")
                
            if os.path.exists(TEST_FILE_PATH):
                logger.info(f"✅ Test file created: {TEST_FILE_PATH}")
                print(f"Test file size: {os.path.getsize(TEST_FILE_PATH)} bytes")
            else:
                logger.error(f"❌ Test file NOT created: {TEST_FILE_PATH}")
            
        except Exception as e:
            logger.error("Error while splitting data")
            raise CustomException("Failed to split data into training and test sets", e)

    def run(self):
        try:
            logger.info("Starting data ingestion process")
            self.download_csv_from_gcp()
            self.split_data()
            logger.info("Data ingestion completed successfully")
        except CustomException as ce:
            logger.error(f"CustomException: {str(ce)}")
        finally:
            logger.info("Data ingestion completed")


if __name__ == "__main__":
    print("DataIngestion class methods:", dir(DataIngestion))
    print("DataIngestion has 'run' method:", hasattr(DataIngestion, 'run'))
    
    if hasattr(DataIngestion, 'run'):
        try:
            print("🔄 Step 1: Reading config...")
            config = read_yaml(CONFIG_PATH)
            print(f"✅ Config loaded: {config}")
            
            print("🔄 Step 2: Creating DataIngestion object...")
            data_ingestion = DataIngestion(config)
            print("✅ DataIngestion object created")
            
            print("🔄 Step 3: Running data ingestion...")
            data_ingestion.run()
            print("✅ Data ingestion completed!")
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("ERROR: DataIngestion class is malformed!")