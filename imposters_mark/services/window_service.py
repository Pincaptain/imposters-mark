from abc import ABC, abstractmethod

from imposters_mark.repositories.window_repository import IWindowRepository


class IWindowService(ABC):
    """
    Abstract class for a window service containing the required
    methods and their signatures.
    """

    @abstractmethod
    def get_window_handle(self, window_name: str) -> int:
        pass

    @abstractmethod
    def get_window_rect(self, window_name: str) -> tuple:
        pass


class WindowService(IWindowService):
    """
    Window service class used to provide the application with the specified window
    handle or window rect (bounding box).
    """

    def __init__(self, window_repository: IWindowRepository):
        """
        Initialize the window service using the provided window repository.

        :param window_repository: Window repository
        """

        self.window_repository = window_repository

    def get_window_handle(self, window_name: str) -> int:
        """
        Using the window repository return the window handle of the window
        with the specified name.

        :param window_name: Window name
        :return: Window handle
        """

        return self.window_repository.get_window_handle(window_name)

    def get_window_rect(self, window_name: str) -> tuple:
        """
        Using the window repository return the window rect (bounding box)
        of the window with the specified name.

        :param window_name: Window name
        :return: Window rect/tuple
        """

        return self.window_repository.get_window_rect(window_name)
