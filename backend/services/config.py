import os

# from pydantic_settings import BaseSettings, SettingsConfigDict
# class Settings(BaseSettings):
#     DB_USER: str
#     DB_PASSWORD: str
#     DB_HOST: str
#     DB_PORT: int
#     DB_NAME: str
#
#     # DATABASE_SQLITE = 'sqlite+aiosqlite:///data/db.sqlite3'
#     model_config = SettingsConfigDict(
#         env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
#     )
#
#     def get_db_url(self):
#         return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
#                 f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")
# #
# settings = Settings()

def is_local_development():
    return not os.path.exists('/.dockerenv')


if is_local_development():
    from dotenv import load_dotenv
    # Загружаем .env из корня проекта (папка env)
    # Путь: backend/services/config.py -> backend -> корень проекта -> env/.env
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_root = os.path.dirname(backend_dir)
    env_path = os.path.join(project_root, 'env', '.env')
    load_dotenv(env_path)
    # Также пробуем загрузить из корня проекта на случай если запускаем оттуда
    load_dotenv(os.path.join(project_root, '.env'))
    # И из папки backend
    load_dotenv(os.path.join(backend_dir, '.env'))


DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_NAME = os.getenv('DB_NAME', 'finances')
SECRET_TOKEN = os.getenv('SECRET_TOKEN', 'your-secret-key-change-in-production')

def get_db_url():
        return (f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@"
                f"{DB_HOST}:{DB_PORT}/{DB_NAME}")
DATABASE_URL = get_db_url()