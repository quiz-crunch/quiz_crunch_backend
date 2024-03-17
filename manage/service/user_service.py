from basic.minio_client.minio_clent import MinioClient
from manage.entity.user import UserEntity
from manage.model.user_model import UserModel
from manage.repository.user_repository import UserRepository


class UserService:
    def __init__(
            self,
            user_repository: UserRepository,
            minio_client: MinioClient
    ):
        self.__user_repository = user_repository
        self.__minio_client = minio_client

    def get_list(self):
        return self.__user_repository.get_list()

    def get_detail(self, user_id: str):
        return self.__user_repository.get_detail(
            user_id=user_id
        )

    def upload(self, file, file_name: str):
        return self.__minio_client.put_object(
            file_name=file_name,
            data=file,
        )

    def add(self, user: UserModel):
        return self.__user_repository.add(
            model=user,
            entity=UserEntity,
        )
