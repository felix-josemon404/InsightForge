from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = "postgresql://felixjosemon:1234567890@localhost:5432/store"

engine = create_engine(DB_URL)
