from dependency_injector import containers, providers

from manage import ManageContainer


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    example_module_container = providers.Container(ManageContainer, config=config)
