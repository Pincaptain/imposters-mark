from abc import ABC, abstractmethod

from imposters_mark.repositories.screen_repository import IScreenRepository


class IScreenService(ABC):
    @abstractmethod
    def get_frame(self):
        pass


class ScreenService(IScreenService):
    def __init__(self, screen_repository: IScreenRepository):
        self.screen_repository = screen_repository

    def get_frame(self):
        return self.screen_repository.get_frame()
