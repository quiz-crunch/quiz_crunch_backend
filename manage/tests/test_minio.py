from minio import Minio

if __name__ == '__main__':
    client = Minio(
        "192.168.10.80:9000",
        access_key="",
        secret_key="",
        secure=False
    )

    bucket_name = ""

    count = 0
    objects = client.list_objects(bucket_name, prefix="", recursive=True)
    for obj in objects:
        count += 1
    print(count)
