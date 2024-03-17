from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import JSONB

from basic.repository.basic_entity import BasicEntity


class UserEntity(BasicEntity):
    __tablename__ = 'ct_user'
    __table_args__ = {"comment": "用户表 - 存储用户基础信息及账户信息"}

    name = Column(String(255), nullable=False, index=True)
    password_hash = Column(String(255), nullable=False, comment="用户密码哈希")
    profile = Column(JSONB, nullable=True, comment="用户个人信息，以 JSONB 格式存储", default={})
    mobile = Column(String(255), nullable=True, comment="用户手机号")
    email = Column(String(255), nullable=True, comment="用户邮箱")
