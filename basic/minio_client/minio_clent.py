import datetime
import hashlib
import os
from datetime import timedelta
from typing import Dict
from minio import Minio


class MinioClient:
    def __init__(self, config: Dict):
        self.__MINIO_DEFAULT_BUCKET_NAME = config["MINIO_DEFAULT_BUCKET_NAME"]
        self.__MINIO_DEFAULT_BUCKET_PATH = config["MINIO_DEFAULT_BUCKET_PATH"]
        self.client = Minio(
            endpoint=config["MINIO_ENDPOINT"],
            access_key=config["MINIO_ACCESS_KEY"],
            secret_key=config["MINIO_SECRET_KEY"],
            secure=config.get("MINIO_SECURE", True)
        )

    def upload_file(self, bucket_name: str, original_name: str, file_path: str):
        object_name = original_name
        self.client.fput_object(bucket_name, object_name, file_path)
        return object_name

    def get_file_url(self, bucket_name: str, object_name: str, expiration: int = 3600):
        time_delta = timedelta(seconds=expiration)
        url = self.client.presigned_get_object(bucket_name, object_name, time_delta)
        return url

    def put_object(self, file_name: str, data, length: int = -1, part_size=10 * 1024 * 1024, bucket_name: str = None,
                   bucket_path: str = None):
        if not bucket_name:
            bucket_name = self.__MINIO_DEFAULT_BUCKET_NAME
        if not bucket_path:
            bucket_path = self.__MINIO_DEFAULT_BUCKET_PATH
        now = datetime.datetime.now()
        formatted_date = now.strftime("%Y-%m-%d_%H-%M-%S")
        random_bytes = os.urandom(4)
        random_str = ''.join([format(byte, '02x') for byte in random_bytes])
        combined_str = formatted_date + random_str
        md5_hash = hashlib.md5(combined_str.encode()).hexdigest()
        object_name = f"{formatted_date}_{md5_hash}_{file_name}"
        full_object_name = f"{bucket_path}/{object_name}"
        res = self.client.put_object(bucket_name=bucket_name, object_name=full_object_name, data=data, length=length,
                                     part_size=part_size)
        return bucket_name, bucket_path, full_object_name, object_name
