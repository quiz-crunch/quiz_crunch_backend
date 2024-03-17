from sqlalchemy import Column, String, func, DateTime, INTEGER, event
from basic import BaseEntity


class BasicEntity(BaseEntity):
    __abstract__ = True  # 将 BasicEntity 设为抽象基类
    id = Column(String(255), primary_key=True, default=func.uuid_generate_v4())
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    version = Column(INTEGER, nullable=False, default=0)


def before_update_listener(_mapper, _connection, target):
    # 自动递增 version 字段
    target.version += 1


# 注册监听函数
event.listen(BasicEntity, 'before_update', before_update_listener)
