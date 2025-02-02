import os
from dotenv import load_dotenv
import sys

# Print the current working directory and sys.path for debugging
print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

# Load the .env file
load_dotenv(verbose=True)

# Get the OPENAI_API_KEY
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Print the API key (be careful with this in production!)
# print(f"OPENAI_API_KEY: {'*' * len(OPENAI_API_KEY) if OPENAI_API_KEY else 'Not set'}")

# Raise an error if the key is not set
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY must be set in the .env file or environment variables")