import importlib
from typing import Dict, TypeVar, Type, Optional, List

from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from basic import BaseEntity

# 创建两个类型变量
T_BaseModel = TypeVar('T_BaseModel', bound=BaseModel)
U_BaseEntity = TypeVar('U_BaseEntity', bound=BaseEntity)


class BaseRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(
            self,
            model: T_BaseModel,
            entity: Type[U_BaseEntity]
    ) -> bool:
        """
        添加记录
        :param model: Pydantic模型类型
        :param entity: SQLAlchemy实体类型
        :return:
        """
        model.convert_names = False
        data_dict = model.model_dump()
        add_data = entity(**data_dict)
        self.session.add(add_data)
        # self.session.flush()  # 这里使用 flush 来立即执行 SQL 但不提交事务
        return True

    def get_model_by_id(
            self,
            entity_id: str,
            entity: Type[U_BaseEntity],
    ) -> Optional[T_BaseModel]:
        """
        根据 id 获取记录
        :param entity_id: 实体的ID
        :param entity: SQLAlchemy实体类型
        :return: Pydantic模型实例或None
        """
        data_dict = self.get_dict_by_id(
            entity_id=entity_id,
            entity=entity
        )
        if data_dict:
            # model名为entity名加上Model，文件名为下划线命名
            model_class_name = entity.__name__ + 'Model'
            module_name = f"app.models.{str(entity.__name__).lower()}_model"
            # 动态导入模块
            models_module = importlib.import_module(module_name)
            # 从模块获取模型类
            model_class = getattr(models_module, model_class_name, None)
            if model_class:
                # 实例化模型类
                model_instance = model_class(**data_dict)
                return model_instance
        return None

    def get_dict_by_id(
            self,
            entity_id: str,
            entity: Type[U_BaseEntity]
    ) -> Optional[Dict]:
        """
        根据 id 获取记录
        :param entity_id: 实体的ID
        :param entity: SQLAlchemy实体类型
        :return: Dict或None
        """
        entity_instance = self.session.query(entity).filter_by(id=entity_id).first()
        if entity_instance:
            # 获取 entity 类中定义的字段名称
            column_names = {column.name for column in entity.__table__.columns}
            # 构造只包含 entity 中定义字段的字典
            data_dict = {key: value for key, value in entity_instance.__dict__.items() if key in column_names}
            return data_dict
        return None

    def get_all_by_id(
            self,
            model: T_BaseModel,
            entity_id: str
    ):
        """
        根据 id 获取所有记录
        :param model:
        :param entity_id:
        :return:
        """
        return self.session.query(model).filter_by(id=entity_id).all()

    def get_by_params(
            self,
            model: Type[T_BaseModel],
            entity: Type[U_BaseEntity] = None,
            params: Optional[Dict] = None,
            sql: Optional[str] = None,
    ) -> Optional[T_BaseModel]:
        """
        根据参数获取记录，并转换为指定的 Pydantic 模型
        :param entity: SQLAlchemy实体类型
        :param model: Pydantic模型类型
        :param params: 查询参数
        :param sql: 自定义SQL查询字符串
        :return: Pydantic模型列表
        """

        if sql:
            # 使用参数化查询执行自定义 SQL
            result = self.session.execute(text(sql), params=params)
            entities = result.fetchall()
            # 针对原生SQL查询结果进行处理
            model_data = model(**entities[0]._asdict()) if entities else None
        else:
            # 根据提供的 params 构建查询
            query = self.session.query(entity)
            if params:
                query = query.filter_by(**params)
            entities = query.all()
            # 将 SQLAlchemy 实体转换为字典，然后构造 Pydantic 模型
            model_data = None
            for ent in entities:
                entity_dict = {column.name: getattr(ent, column.name, None) for column in ent.__table__.columns}
                model_instance = model(**entity_dict)
                model_data = model_instance
                break

        return model_data

    def get_all_by_params(
            self,
            model: Type[T_BaseModel],
            entity: Type[U_BaseEntity] = None,
            params: Optional[Dict] = None,
            sql: Optional[str] = None,
    ) -> List[T_BaseModel]:
        """
        根据参数获取记录，并转换为指定的 Pydantic 模型
        :param entity: SQLAlchemy实体类型
        :param model: Pydantic模型类型
        :param params: 查询参数
        :param sql: 自定义SQL查询字符串
        :return: Pydantic模型列表
        """

        if sql:
            # 使用参数化查询执行自定义 SQL
            result = self.session.execute(text(sql), params=params)
            entities = result.fetchall()
            # 针对原生SQL查询结果进行处理
            model_list = [model(**row._asdict()) for row in entities]
        else:
            # 根据提供的 params 构建查询
            query = self.session.query(entity)
            if params:
                query = query.filter_by(**params)
            entities = query.all()
            # 将 SQLAlchemy 实体转换为字典，然后构造 Pydantic 模型
            model_list = []
            for ent in entities:
                entity_dict = {column.name: getattr(ent, column.name, None) for column in ent.__table__.columns}
                model_instance = model(**entity_dict)
                model_list.append(model_instance)

        return model_list

    def update(
            self,
            model: T_BaseModel,
            entity_id: str,
            data
    ):
        """
        更新记录
        :param model:
        :param entity_id:
        :param data:
        :return:
        """
        pass

    def delete(self, entity: Type[U_BaseEntity], entity_id: str):
        """
        删除记录
        :param entity: 实体类
        :param entity_id: 要删除的实体的 ID
        :return: None
        """
        model = self.get_model_by_id(entity_id=entity_id, entity=entity)
        if model:
            # 删除该实体
            self.session.delete(model)
            # self.session.flush()
            self.session.commit()
        else:
            # 如果没有找到实体，可以抛出异常或处理该情况
            raise Exception(f"未找到 ID 为 {entity_id} 的 {entity.__name__} 实体")

    def execute_sql(self, sql, params: Dict):
        """
        执行 sql 语句并返回结果
        :param sql: SQL语句
        :param params: SQL参数
        :return: 查询结果
        """
        result = self.session.execute(text(sql), params)
        # self.session.flush()

        # 如果是SELECT查询，返回所有结果
        if sql.strip().lower().startswith("select"):
            return result.fetchall()

        # 对于非SELECT查询，返回影响的行数
        else:
            return result.rowcount
