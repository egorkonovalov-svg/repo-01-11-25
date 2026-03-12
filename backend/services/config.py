import os


def is_local_development():
    return not os.path.exists('/.dockerenv')


if is_local_development():
    from dotenv import load_dotenv

    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_root = os.path.dirname(backend_dir)

    load_dotenv(os.path.join(project_root, 'env', '.env'))
    load_dotenv(os.path.join(project_root, '.env'))
    load_dotenv(os.path.join(backend_dir, '.env'))


DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
SECRET_TOKEN = os.getenv('SECRET_TOKEN')

DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
