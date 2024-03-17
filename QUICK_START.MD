## 1.将项目代码clone到本地

```shell
git clone https://github.com/547414/python_web_backend_framework.git
```

## 2.安装python

[python安装包下载](https://www.python.org/downloads/)

## 3.安装poetry

cmd或者shell进入到python根目录\Scripts，执行以下命令

```shell
pip install poetry
```

## 4.配置虚拟环境

为啥配置虚拟环境？因为不同的项目可能需要不同的依赖，为了避免依赖冲突，所以需要配置虚拟环境

以pycharm为例
![poetry_env.png](./doc/quick_start/poetry_env.png "add poetry env")

## 5.安装依赖

项目基于python3.10进行开发，如果需要更换更低的python版本，需要在pyproject.toml文件中修改python版本, 然后执行poetry update

```toml
[tool.poetry.dependencies]
python = "^3.9"
```

```shell
poetry update
```

如果不需要更换python版本，直接执行以下命令

```shell
poetry install --no-root
```

![poetry_install.png](./doc/quick_start/poetry_install.png "poetry install")

## 6.配置启动参数

以pycharm为例
![config.png](./doc/quick_start/config.png "config")

## 7.安装postgresql

[postgresql安装包下载](https://www.postgresql.org/download/)

## 8.配置数据库

以windows为例，第7步安装postgresql的时候，会自动安装pgAdmin4
![create_database.png](./doc/quick_start/create_database.png "create database")
运行 项目根目录/example_module/tests/test_generate_data_table.py文件，生成数据库表
![generate_database_table.png](./doc/quick_start/generate_database_table.png "generate database table")

## 9.配置项目根目录下的.env文件

```shell
DATABASE_URL=postgresql://user:password@127.0.0.1:5432/python_web_backend_framework
```

## 10.安装并启动minio

[MinIO官网安装步骤](https://min.io/download#/windows)
以windows为例，在powershell中执行以下命令

```shell
Invoke-WebRequest -Uri "https://dl.min.io/server/minio/release/windows-amd64/minio.exe" -OutFile "C:\minio.exe"
setx MINIO_ROOT_USER admin
setx MINIO_ROOT_PASSWORD password
C:\minio.exe server F:\Data --console-address ":9001"
```

## 11.配置minio

创建一个bucket
![create_bucket.png](./doc/quick_start/create_bucket.png "create bucket")
创建access_key
![create_access_key.png](./doc/quick_start/create_access_key.png "create access key")
配置项目根目录下的.env文件

```shell
MINIO_ENDPOINT=127.0.0.1:9000
MINIO_DEFAULT_BUCKET_NAME=example-bucket
MINIO_DEFAULT_BUCKET_PATH=/common
MINIO_ACCESS_KEY=xxx
MINIO_SECRET_KEY=xxx
MINIO_SECURE=false
```

## 12.启动项目

以pycharm为例，点击run或者debug
![run.png](./doc/quick_start/run.png "run")
以pycharm为例，如下图所示，项目启动成功
![start_success.png](./doc/quick_start/start_success.png "start success")