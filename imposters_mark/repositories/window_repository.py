from abc import ABC, abstractmethod

import win32gui


class WindowRepositoryHelper(object):
    """
    Static class that provides the window repository class with the required
    methods using the win32 api.
    """

    t_window_handle = None
    t_window_rect = None

    @staticmethod
    def get_window_handle(window_name: str) -> int:
        """
        Iterate over the windows and get the handle of the one with
        the requested name.

        :param window_name: Window name
        :return: Window handle int
        """

        win32gui.EnumWindows(WindowRepositoryHelper.__iterate_windows, window_name)

        return WindowRepositoryHelper.t_window_handle

    @staticmethod
    def get_window_rect(window_name: str) -> tuple:
        """
        Iterate over the windows and get the rect of the one with
        the requested name.

        :param window_name: Window name
        :return: Window rect tuple
        """
        win32gui.EnumWindows(WindowRepositoryHelper.__iterate_windows, window_name)

        return WindowRepositoryHelper.t_window_rect

    @staticmethod
    def __iterate_windows(window_handle, window_name):
        """
        Foreach window if the window name matches the requested name
        update the static class variables to the current window.

        :param window_handle: Window handle
        :param window_name: Window name
        """
        t_window_name = win32gui.GetWindowText(window_handle)

        if t_window_name == window_name:
            WindowRepositoryHelper.t_window_handle = window_handle
            WindowRepositoryHelper.t_window_rect = win32gui.GetWindowRect(window_handle)


class IWindowRepository(ABC):
    """
    Abstract class for a window repository containing the required
    methods and their signatures.

    I encourage you to create a custom implementation of the
    window repository class that will not depend on a static helper
    class for the win32 api methods.
    """

    @abstractmethod
    def get_window_handle(self, window_name: str) -> int:
        pass

    @abstractmethod
    def get_window_rect(self, window_name: str) -> tuple:
        pass


class WindowRepository(IWindowRepository):
    """
    Window repository class used to obtain a window handle (int) or
    a window rect (bounding rectangle of a window).
    """

    # noinspection PyMethodMayBeStatic
    def get_window_handle(self, window_name: str) -> int:
        """
        Using the helper class obtain the window handle using the
        requested window name.

        :param window_name: Window name
        :return: Window handle int
        """

        return WindowRepositoryHelper.get_window_handle(window_name)

    # noinspection PyMethodMayBeStatic
    def get_window_rect(self, window_name: str) -> tuple:
        """
        Using the helper class obtain the window rect using the
        requested window name.

        :param window_name: Window name
        :return: Window rect tuple
        """

        return WindowRepositoryHelper.get_window_rect(window_name)
