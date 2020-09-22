from abc import ABC, abstractmethod

import numpy
import cv2
from PIL import ImageGrab

from imposters_mark.repositories.window_repository import IWindowRepository


class IScreenRepository(ABC):
    @abstractmethod
    def get_frame(self):
        pass


class ScreenRepository(IScreenRepository):
    def __init__(self, window_repository: IWindowRepository):
        self.window_repository = window_repository

    def get_frame(self):
        window_rect = self.window_repository.get_window_rect()
        window_image = ImageGrab.grab(bbox=window_rect)
        window_image_arr = numpy.array(window_image)

        return cv2.cvtColor(window_image_arr, cv2.COLOR_BGR2RGB)
