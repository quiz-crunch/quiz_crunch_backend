from config import Config
from manage.manage_container import ManageContainer

manage_container = ManageContainer()
manage_container.config.from_dict(Config().model_dump())

manage_container.wire(packages=[__name__])
