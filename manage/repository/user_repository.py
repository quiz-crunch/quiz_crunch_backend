from sqlalchemy.orm import Session

from basic.repository.base_repository import BaseRepository
from manage.entity.user import UserEntity
from manage.model.user_model import UserModel


class UserRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def get_list(self):
        return self.get_all_by_params(
            entity=UserEntity,
            model=UserModel
        )

    def get_detail(self, user_id: str):
        sql = """
        SELECT * FROM ct_user WHERE id = :user_id
        """
        return self.get_by_params(
            model=UserModel,
            sql=sql,
            params={
                "user_id": user_id
            }
        )
