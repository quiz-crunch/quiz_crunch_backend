from sqlalchemy import Column, String, func, DateTime, Text
from sqlalchemy.dialects.postgresql import JSONB

from basic.repository.basic_entity import BasicEntity


class BasicHistoryEntity(BasicEntity):
    __abstract__ = True  # 将 BasicHistoryEntity 设为抽象基类
    history_id = Column(String(255), primary_key=True, default=func.uuid_generate_v4(), comment="主键")
    operate_at = Column(DateTime(timezone=True), default=func.now(), comment="更新时间")
    operate_type = Column(String(50), nullable=False, comment="更新类型")
    operator_category = Column(String(255), nullable=False, comment="操作者类型")
    operator = Column(String(255), nullable=False, comment="操作者")
    start_time = Column(DateTime(timezone=True), default=func.now(), comment="开始时间")
    end_time = Column(DateTime(timezone=True), nullable=True, comment="结束时间")
    comment = Column(Text, nullable=True, comment="备注")
    snapshot = Column(JSONB, nullable=True, comment="快照")
    change_details = Column(JSONB, nullable=True, comment="变更详情")
