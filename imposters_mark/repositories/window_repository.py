from abc import ABC, abstractmethod

import win32gui


class WindowRepositoryHelper(object):
    t_window_handle = None
    t_window_rect = None
    t_window_set = False

    @staticmethod
    def get_window_handle(window_name: str) -> int:
        WindowRepositoryHelper.t_window_set = False
        win32gui.EnumWindows(WindowRepositoryHelper.__iterate_windows, window_name)

        return WindowRepositoryHelper.t_window_handle

    @staticmethod
    def get_window_rect(window_name: str) -> tuple:
        WindowRepositoryHelper.t_window_set = False
        win32gui.EnumWindows(WindowRepositoryHelper.__iterate_windows, window_name)

        return WindowRepositoryHelper.t_window_rect

    @staticmethod
    def __iterate_windows(window_handle, window_name):
        t_window_name = win32gui.GetWindowText(window_handle)

        if t_window_name == window_name and not WindowRepositoryHelper.t_window_set:
            WindowRepositoryHelper.t_window_handle = window_handle
            WindowRepositoryHelper.t_window_rect = win32gui.GetWindowRect(window_handle)
            WindowRepositoryHelper.t_window_set = True


class IWindowRepository(ABC):
    @abstractmethod
    def get_window_handle(self) -> int:
        pass

    @abstractmethod
    def get_window_rect(self) -> tuple:
        pass


class WindowRepository(IWindowRepository):
    def __init__(self, window_name: str):
        self.window_name = window_name

    def get_window_handle(self) -> int:
        return WindowRepositoryHelper.get_window_handle(self.window_name)

    def get_window_rect(self) -> tuple:
        return WindowRepositoryHelper.get_window_rect(self.window_name)
