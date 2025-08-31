import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Email configuration from environment variables
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "your_email@gmail.com")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL", "recipient@example.com")
APP_PASSWORD = os.getenv("APP_PASSWORD", "your_app_password") 