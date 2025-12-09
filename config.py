# config.py
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
SCRAPINGANT_KEY = os.getenv("SCRAPINGANT_KEY")
