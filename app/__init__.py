import importlib
import os

from flask import Flask
from app.containers import Container
from config import Config

container = Container()
container.config.from_dict(Config().model_dump())


def register_blueprints(app: Flask):
    blueprints_dir = os.path.join(app.root_path, 'blueprint')
    for filename in os.listdir(blueprints_dir):
        if filename.endswith('_blueprint.py'):
            module_name = f'app.blueprint.{filename[:-3]}'
            mod = importlib.import_module(module_name)
            if hasattr(mod, 'bp'):
                app.register_blueprint(mod.bp, url_prefix=f'/api/{filename[:-13]}')


def create_app() -> Flask:
    app = Flask(__name__)
    app.container = container
    # 创建数据库表
    # BaseEntity.metadata.create_all(bind=container.engine())

    # https://github.com/ets-labs/python-dependency-injector/issues/328#issuecomment-734040664
    container.wire(packages=[__name__])

    # 注册app.blueprints中以 _blueprint.py 结尾的蓝图
    register_blueprints(app)

    return app
