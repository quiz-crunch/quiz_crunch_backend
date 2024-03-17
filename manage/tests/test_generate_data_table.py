import os
import importlib

from basic import BaseEntity
import manage.entity as entity_module
from manage import manage_container


def import_entities_from_directory(directory, base_package):
    """
    递归扫描指定目录下的所有Python文件（排除__init__.py），并导入它们。

    :param directory: 要扫描的目录
    :param base_package: 基础包名，用于构建完整的模块路径
    """
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.py') and filename != '__init__.py':
                # 构建模块的相对路径
                relative_path = os.path.relpath(root, directory)
                # 替换路径分隔符为点，构建完整的模块名
                if relative_path == '.':
                    module_name = f'{base_package}.{filename[:-3]}'
                else:
                    module_name = f'{base_package}.{relative_path.replace(os.sep, ".")}.{filename[:-3]}'
                print(module_name)
                importlib.import_module(module_name)


if __name__ == '__main__':
    entity_module_path = os.path.dirname(entity_module.__file__)

    # 导入 manage.entity 下的所有 Python 文件
    import_entities_from_directory(entity_module_path, 'manage.entity')

    # 创建表
    BaseEntity.metadata.create_all(manage_container.engine())
