#utils/comfig.py

import os
from dotenv import load_dotenv
load_dotenv()

GDRIVE_FOLDER_ID = os.getenv("GDRIVE_FOLDER_ID")
CREDENTIALS_FILE = os.getenv("GOOGLE_DRIVE_CREDENTIALS")
ELASTIC_HOST = os.getenv("ELASTIC_HOST", "http://localhost:9200")