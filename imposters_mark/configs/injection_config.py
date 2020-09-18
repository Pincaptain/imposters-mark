from dependency_injector import containers, providers

from imposters_mark.repositories.window_repository import WindowRepository
from imposters_mark.repositories.screen_repository import ScreenRepository
from imposters_mark.services.window_service import WindowService
from imposters_mark.services.screen_service import ScreenService


class Container(containers.DeclarativeContainer):
    """
    Declarative container containing the instances of the
    singletons and their configuration.
    """

    config = providers.Configuration()
    window_repository = providers.Singleton(WindowRepository)
    screen_repository = providers.Singleton(ScreenRepository, window_repository=window_repository)
    window_service = providers.Singleton(WindowService, window_repository=window_repository)
    screen_service = providers.Singleton(ScreenService, screen_repository=screen_repository)


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

    def get_screen_repository(self) -> ScreenRepository:
        """
        Return the screen repository singleton.

        :return: Screen repository singleton
        """

        return self.container.screen_repository()

    def get_window_service(self) -> WindowService:
        """
        Return the window service singleton.

        :return: Window service singleton
        """

        return self.container.window_service()

    def get_screen_service(self) -> ScreenService:
        """
        Return the screen service singleton.

        :return: Screen service singleton
        """

        return self.container.screen_service()
