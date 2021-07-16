from dotenv import load_dotenv
import os

load_dotenv()

API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
SESSION = os.environ.get('SESSION')
CONNECTION_STRING = os.environ.get('CONNECTION_STRING')
