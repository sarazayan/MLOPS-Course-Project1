import os
from config.paths_config import *

print("=== PATH DEBUGGING ===")
print(f"Current working directory: {os.getcwd()}")
print(f"RAW_DIR: {RAW_DIR}")
print(f"RAW_FILE_PATH: {RAW_FILE_PATH}")
print(f"TRAIN_FILE_PATH: {TRAIN_FILE_PATH}")
print(f"TEST_FILE_PATH: {TEST_FILE_PATH}")

print("\n=== DIRECTORY EXISTENCE ===")
print(f"RAW_DIR exists: {os.path.exists(RAW_DIR)}")
print(f"TRAIN_FILE_PATH parent dir exists: {os.path.exists(os.path.dirname(TRAIN_FILE_PATH))}")
print(f"TEST_FILE_PATH parent dir exists: {os.path.exists(os.path.dirname(TEST_FILE_PATH))}")

print("\n=== FILE EXISTENCE ===")
print(f"RAW_FILE_PATH exists: {os.path.exists(RAW_FILE_PATH)}")
print(f"TRAIN_FILE_PATH exists: {os.path.exists(TRAIN_FILE_PATH)}")
print(f"TEST_FILE_PATH exists: {os.path.exists(TEST_FILE_PATH)}")

if os.path.exists(RAW_FILE_PATH):
    print(f"RAW file size: {os.path.getsize(RAW_FILE_PATH)} bytes")

print("\n=== ARTIFACTS FOLDER CONTENTS ===")
artifacts_dir = os.path.join(os.getcwd(), "artifacts")
print(f"Artifacts directory: {artifacts_dir}")
print(f"Artifacts exists: {os.path.exists(artifacts_dir)}")

if os.path.exists(artifacts_dir):
    print("Contents of artifacts folder:")
    for item in os.listdir(artifacts_dir):
        item_path = os.path.join(artifacts_dir, item)
        if os.path.isfile(item_path):
            print(f"  FILE: {item} ({os.path.getsize(item_path)} bytes)")
        else:
            print(f"  DIR:  {item}")
else:
    print("Artifacts folder does not exist!")

print("\n=== SEARCHING FOR CSV FILES ===")
for root, dirs, files in os.walk(os.getcwd()):
    for file in files:
        if file.endswith('.csv'):
            full_path = os.path.join(root, file)
            size = os.path.getsize(full_path)
            print(f"Found CSV: {full_path} ({size} bytes)")