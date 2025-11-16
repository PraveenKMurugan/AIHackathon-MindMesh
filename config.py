import os
from dotenv import load_dotenv

load_dotenv()  # loads .env file

VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH")
DATA_PATH = os.getenv("DATA_PATH")
CLEANED_PATH = os.getenv("CLEANED_PATH")

CONFLUENCE_BASE_URL = os.getenv("CONFLUENCE_BASE_URL")
CONFLUENCE_EMAIL = os.getenv("CONFLUENCE_EMAIL")
CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
