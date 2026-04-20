import sys
import os

# Add project directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Load env vars
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from app import create_app

application = create_app("production")
