import os
from pathlib import Path
from dotenv import load_dotenv

current_file = Path(__file__).resolve()
base_dir = current_file.parent.parent
env_path = base_dir / ".env"

load_dotenv(dotenv_path=env_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError(f"❌ GEMINI_API_KEY is missing inside {env_path}")

CLEANED_GEMINI_KEY = GEMINI_API_KEY.strip().replace('"', "").replace("'", "")

os.environ["GEMINI_API_KEY"] = CLEANED_GEMINI_KEY
os.environ["GOOGLE_API_KEY"] = CLEANED_GEMINI_KEY

POSTGRES_URL = os.getenv("POSTGRES_URL")
if not POSTGRES_URL:
    raise ValueError("POSTGRES_URL is missing from the .env file")

PDF_PATH = r"C:\Python\GEN AI\app\employee_policy_handbook_complete.pdf"
QDRANT_URL = "http://localhost:6333"
QDRANT_COLLECTION = "learning_rag"