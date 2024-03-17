import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Config(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    MINIO_ENDPOINT: str = os.getenv('MINIO_ENDPOINT')
    MINIO_DEFAULT_BUCKET_PATH: str = os.getenv('MINIO_DEFAULT_BUCKET_PATH')
    MINIO_DEFAULT_BUCKET_NAME: str = os.getenv('MINIO_DEFAULT_BUCKET_NAME')
    MINIO_ACCESS_KEY: str = os.getenv('MINIO_ACCESS_KEY')
    MINIO_SECRET_KEY: str = os.getenv('MINIO_SECRET_KEY')
    MINIO_SECURE: bool = os.getenv('MINIO_SECURE')
