from dependency_injector import containers, providers

from imposters_mark.repositories.window_repository import WindowRepository
from imposters_mark.repositories.screen_repository import ScreenRepository
from imposters_mark.services.screen_service import ScreenService
from imposters_mark.services.game_service import GameService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    window_repository = providers.Singleton(WindowRepository, window_name=config.general.window_name)
    screen_repository = providers.Singleton(ScreenRepository, window_repository=window_repository)

    screen_service = providers.Singleton(ScreenService, screen_repository=screen_repository)
    game_service = providers.Singleton(GameService, screen_service=screen_service,
                                       pytesseract_cmd=config.general.pytesseract_cmd)


class InjectionConfig(object):
    def __init__(self, config_path: str):
        self.container = Container()
        self.container.config.from_ini(config_path)

    def get_window_repository(self) -> WindowRepository:
        return self.container.window_repository()

    def get_screen_repository(self) -> ScreenRepository:
        return self.container.screen_repository()

    def get_screen_service(self) -> ScreenService:
        return self.container.screen_service()

    def get_game_service(self) -> GameService:
        return self.container.game_service()
