from abc import ABC, abstractmethod
from datetime import datetime

import cv2
import numpy

from imposters_mark.repositories.screen_repository import IScreenRepository


class _FrameHelper(object):
    @staticmethod
    def draw_lines(frame):
        grayscale = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(grayscale, 30, 100)
        lines = cv2.HoughLinesP(edges, 1, numpy.pi / 180, 60, numpy.array([]), 50, 5)

        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)

        return frame

    @staticmethod
    def draw_contours(frame):
        grayscale = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        thresh = 100
        ret, thresh_frame = cv2.threshold(grayscale, thresh, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        frame = cv2.drawContours(frame, contours, -1, (0, 0, 255), 1)

        return frame

    @staticmethod
    def o_draw_contours(frame):
        grayscale = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        thresh = 100
        ret, thresh_frame = cv2.threshold(grayscale, thresh, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        frame = numpy.zeros(frame.shape)
        frame = cv2.drawContours(frame, contours, -1, (0, 0, 255), 1)

        return frame


class IScreenService(ABC):
    """
    Abstract class for a screen service containing the required
    methods and their signatures.

    Implementation of a custom service class for screen service should
    be done only in case you want to add additional features in between.
    """

    @abstractmethod
    def get_screen(self, window_name: str):
        pass


class ScreenService(IScreenService):
    """
    Screen service class used to obtain the frame of a window using the
    provided window repository and window name.

    Additionally this class is used to paint the required shapes or text
    over the obtained frame.
    """

    def __init__(self, screen_repository: IScreenRepository):
        """
        Initialize the screen repository provided.

        :param screen_repository: Screen repository
        """

        self.screen_repository = screen_repository

    def get_screen(self, window_name: str):
        """
        Get the screen frame using the screen repository, paint the
        required shapes/text over it and return it.

        :param window_name: Window name
        :return: Window frame
        """

        window_frame = self.screen_repository.get_screen(window_name)
        window_frame_height, window_frame_width, window_frame_channels = window_frame.shape

        window_frame = _FrameHelper.o_draw_contours(window_frame)

        time_text = str(datetime.now())
        time_text_position = (20, window_frame_height - 20)
        time_text_font = cv2.FONT_HERSHEY_PLAIN
        time_text_color = (0, 0, 255)

        window_frame = cv2.putText(window_frame, time_text, time_text_position, time_text_font, 1, time_text_color, 2)

        version_text = 'Imposters Mark v0.1'
        version_text_position = (20, window_frame_height - 40)
        version_text_font = cv2.FONT_HERSHEY_PLAIN
        version_text_color = (0, 0, 255)

        window_frame = cv2.putText(window_frame, version_text, version_text_position, version_text_font, 1,
                                   version_text_color, 2)

        return window_frame
