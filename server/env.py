import os
from dotenv import load_dotenv
load_dotenv()

CLIENT_URL = os.getenv("CLIENT_BASE_URL")
DATABASE_URL = os.getenv("DB_HOST")
HUGGINGFACEHUB_API_TOKEN= os.getenv("HUGGINGFACEHUB_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")