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
    load_dotenv()


DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

def get_db_url():
        return (f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@"
                f"{DB_HOST}:{DB_PORT}/{DB_NAME}")
DATABASE_URL = get_db_url()