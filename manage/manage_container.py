from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from basic.minio_client.minio_clent import MinioClient
from basic.repository.unit_of_work import UnitOfWork
from manage.repository.user_repository import UserRepository
from manage.service.user_service import UserService


class ManageContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    # https://python-dependency-injector.ets-labs.org/examples/fastapi-sqlalchemy.html
    engine = providers.Singleton(create_engine, url=config.SQLALCHEMY_DATABASE_URI)
    Session = providers.ThreadLocalSingleton(sessionmaker, bind=engine)
    session = providers.Singleton(scoped_session, Session)
    # Minio 客户端配置
    minio_client = providers.Singleton(
        MinioClient,
        config=config
    )

    # 配置 UnitOfWork
    unit_of_work = providers.Factory(UnitOfWork, session_factory=session)

    user_repository = providers.Factory(
        UserRepository,
        session=session,
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
        minio_client=minio_client,
    )
