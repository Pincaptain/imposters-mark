from abc import ABC, abstractmethod

import numpy
import cv2
from PIL import ImageGrab

from imposters_mark.repositories.window_repository import IWindowRepository


class IScreenRepository(ABC):
    """
    Abstract class for a screen repository containing the required
    methods and their signatures.
    """

    @abstractmethod
    def get_screen(self, window_name: str):
        pass


class ScreenRepository(IScreenRepository):
    """
    Screen repository class used to provide the application with a screen frame
    of a window with the specified name.
    """

    def __init__(self, window_repository: IWindowRepository):
        """
        Initialize the window repository provided.

        :param window_repository: Window repository
        """

        self.window_repository = window_repository

    def get_screen(self, window_name: str):
        """
        Return a window frame using the calculated window
        rect from the provided window name.

        :param window_name: Window name
        :return: Window frame
        """

        window_rect = self.window_repository.get_window_rect(window_name)
        window_image = ImageGrab.grab(bbox=window_rect)
        window_image_arr = numpy.array(window_image)

        return cv2.cvtColor(window_image_arr, cv2.COLOR_BGR2RGB)
