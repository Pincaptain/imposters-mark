from dependency_injector import containers, providers

from imposters_mark.repositories.window_repository import WindowRepository


class Container(containers.DeclarativeContainer):
    """
    Declarative container containing the instances of the
    singletons and their configuration.
    """

    config = providers.Configuration()
    window_repository = providers.Singleton(WindowRepository)


class InjectionConfig(object):
    """
    Config class that initializes the container and uses the provided
    configuration to initialize the singletons.
    """

    def __init__(self):
        """
        Initialize the container.
        """

        self.container = Container()

    def get_window_repository(self) -> WindowRepository:
        """
        Return the window repository singleton.

        :return: Window repository singleton
        """

        return self.container.window_repository()
