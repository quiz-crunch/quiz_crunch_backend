from contextlib import contextmanager

from sqlalchemy import func, event

from basic import BaseEntity


class UnitOfWork:
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self.session = None
        self.register_after_flush_listener()

    def __enter__(self):
        self.session = self.session_factory()
        return self

    def __exit__(self, type, value, traceback):
        if type is not None:
            self.rollback()
        self.session.close()

    def commit(self):
        self.session.commit()

    def register_after_flush_listener(self):
        @event.listens_for(self.session_factory(), "after_flush")
        def after_flush(session, context):
            for instance in session.new:
                self.record_history(instance, 'INSERT')
            for instance in session.dirty:
                self.record_history(instance, 'UPDATE')
            for instance in session.deleted:
                self.record_history(instance, 'DELETE')

    def rollback(self):
        self.session.rollback()

    @contextmanager
    def start(self):
        if self.session is not None:
            raise RuntimeError("Session already started")
        self.session = self.session_factory()
        try:
            yield self.session
            self.commit()
        except Exception:
            self.rollback()
            raise
        finally:
            self.session.close()
            self.session = None

    def record_history(self, entity, operation_type):
        """
        记录历史数据 待完善
        :param entity:
        :param operation_type:
        :return:
        """
        history_table_name = "ct_" + entity.__class__.__name__.lower().replace("entity", "") + '_history'
        history_table = BaseEntity.metadata.tables[history_table_name]
        # 在这里构建历史数据，确保使用变更前的状态
        history_data = {
            'history_id': func.uuid_generate_v4(),
            'operate_at': func.now(),
            'operate_type': operation_type,
            'operator_category': 'USER',
            'operator': '123',
        }

        # 如果是INSERT或DELETE，直接从实体提取数据；
        # 对于UPDATE，可能需要特殊处理以获取变更前的数据。
        if operation_type in ['INSERT', 'DELETE']:
            entity_data = {column.name: getattr(entity, column.name) for column in entity.__table__.columns}
            history_data.update(entity_data)
        elif operation_type == 'UPDATE':
            # 对于UPDATE操作，确保捕获变更前的数据状态
            # 这里的实现依赖于你的具体逻辑
            pass

        # 使用传入的session执行插入操作
        self.session.execute(history_table.insert().values(**history_data))
