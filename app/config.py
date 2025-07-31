from dotenv import load_dotenv
import os

load_dotenv() # read file .env

DB_USER = os.getenv("DATABASE_USERNAME")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD")
DB_HOST = os.getenv("DATABASE_HOSTNAME")
DB_PORT = os.getenv("DATABASE_PORT")
DB_NAME = os.getenv("DATABASE_NAME")

DATABASE_URL = (
    f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

SECRET_KEY = os.getenv("JWT_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ALGORITHM = os.getenv("ALGORITHM_TOKEN")
ACCESS_TOKEN_EXPIRES_MINUTES = 30
REFRESH_TOKEN_EXPIRES_MINUTES = 15 * 24 * 60  # 15 days

# redis
REDIS_URL = os.getenv("REDIS_URL")
USERNAME_REDIS_CLOUD = os.getenv("USERNAME_REDIS_CLOUD")
PASSWORD_REDIS_CLOUD = os.getenv("PASSWORD_REDIS_CLOUD")

# payload
REFRESH_COOKIE_NAME = "refresh"
SUB = "sub"
EXP = "exp"
IAT = "iat"
JTI = "jti"

CONTENT_PROMPT_SUMMARY_MESSAGES = "You are an AI assistant that helps users manage the context of long conversations. Your task is to read a sequence of messages between the user and the system, then generate a concise yet comprehensive summary (`summary_context`) that preserves the essential information needed for future interactions, without requiring a full review of the entire message history."
CONTENT_PROMPT_TITLE_MESSAGES="You are an AI assistant tasked with generating a short and clear title for a chat session. Read the conversation and create a concise title (maximum 8 words) that captures the main topic or purpose of the discussion. Focus on making the first few words meaningful and informative, as they will be shown in the UI preview."