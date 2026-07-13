import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'waffle-secret-key-12345')
    
    # MySQL Database Settings
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    DB_NAME = os.environ.get('DB_NAME', 'waffle_pos')
    
    # Option to manually force SQLite fallback for testing without a local MySQL server
    USE_SQLITE = os.environ.get('USE_SQLITE', 'false').lower() == 'true'

    @classmethod
    def get_mysql_base_uri(cls):
        """Returns connection URI without the database name (used for creating the database if it doesn't exist)."""
        password_part = f":{cls.DB_PASSWORD}" if cls.DB_PASSWORD else ""
        return f"mysql+pymysql://{cls.DB_USER}{password_part}@{cls.DB_HOST}:{cls.DB_PORT}"

    @classmethod
    def get_sqlalchemy_database_uri(cls):
        if cls.USE_SQLITE:
            db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'waffle_pos.db'))
            return f"sqlite:///{db_path}"
        
        password_part = f":{cls.DB_PASSWORD}" if cls.DB_PASSWORD else ""
        return f"mysql+pymysql://{cls.DB_USER}{password_part}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
