from abc import ABC, abstractmethod
import threading

import pytesseract
from PIL import ImageGrab
import cv2

from imposters_mark.services.screen_service import ScreenService
from imposters_mark.entities.stats import Stats
from imposters_mark.entities.player import Player


class _PytesseractHelper(object):
    def __init__(self, pytesseract_cmd: str):
        pytesseract.pytesseract.tesseract_cmd = pytesseract_cmd

    # noinspection PyMethodMayBeStatic
    def frame_to_string(self, bbox=None) -> str:
        frame = ImageGrab.grab(bbox)
        string = pytesseract.image_to_string(frame)

        return string.strip()

    # noinspection PyMethodMayBeStatic
    def frame_to_data(self, bbox=None) -> list:
        frame = ImageGrab.grab(bbox)
        content = pytesseract.image_to_data(frame)
        lines = content.splitlines()[1:]
        data = []

        for line in lines:
            line_data = line.split()
            if len(line_data) == 11:
                continue

            data.append({
                'level': line_data[0],
                'page_num': line_data[1],
                'block_num': line_data[2],
                'par_num': line_data[3],
                'line_num': line_data[4],
                'word_num': line_data[5],
                'left': line_data[6],
                'top': line_data[7],
                'width': line_data[8],
                'height': line_data[9],
                'conf': line_data[10],
                'text': line_data[11]})

        return data


class IGameService(ABC):
    @abstractmethod
    def update(self):
        pass


class GameService(IGameService):
    def __init__(self, screen_service: ScreenService, pytesseract_cmd: str):
        self.screen_service = screen_service
        self.pytesseract_helper = _PytesseractHelper(pytesseract_cmd)
        self.stats = Stats()

    def update(self):
        frame = self.screen_service.get_frame()

        update_location = threading.Thread(target=self.__update_location, args=(frame,))
        update_location.start()

        update_players = threading.Thread(target=self.__update_players)
        update_players.start()

        self.__update_thread_count_text(frame)
        self.__update_location_text(frame, 3)
        self.__update_current_location_text(frame)
        self.__update_players_text(frame, 3)
        self.__update_players_rect(frame)

        return frame

    def __update_location(self, frame):
        self.stats.thread_count += 1
        frame_height, frame_width, _ = frame.shape
        bbox = (
            int(frame_width / 4),
            frame_height - 100,
            int(frame_width / 2 + frame_width / 4),
            frame_height - 25)

        location = self.pytesseract_helper.frame_to_string(bbox=bbox)
        self.stats.append_location(location)
        self.stats.thread_count -= 1

    def __update_thread_count_text(self, frame):
        frame_height, frame_width, _ = frame.shape
        thread_count = f'Active Threads: {str(self.stats.thread_count)}'
        position = (10, frame_height - 10)
        font = cv2.QT_FONT_NORMAL
        font_scale = 1
        font_color = (0, 0, 255)
        font_thickness = 3

        cv2.putText(frame, thread_count, position, font, font_scale, font_color, font_thickness)

    def __update_location_text(self, frame, count: int):
        frame_height, frame_width, _ = frame.shape
        location = f'Locations: {self.stats.get_last_locations(count)}'
        position = (10, frame_height - 60)
        font = cv2.QT_FONT_NORMAL
        font_scale = 1
        font_color = (0, 0, 255)
        font_thickness = 3

        cv2.putText(frame, location, position, font, font_scale, font_color, font_thickness)

    def __update_current_location_text(self, frame):
        frame_height, frame_width, _ = frame.shape
        current_location = f'Current Location: {self.stats.get_current_location()}'
        position = (10, frame_height - 110)
        font = cv2.QT_FONT_NORMAL
        font_scale = 1
        font_color = (0, 0, 255)
        font_thickness = 3

        cv2.putText(frame, current_location, position, font, font_scale, font_color, font_thickness)

    def __update_players(self):
        self.stats.thread_count += 1
        data = self.pytesseract_helper.frame_to_data()

        for entry in data:
            player = Player()
            player.name = entry['text']
            player.position = (
                int(entry['left']),
                int(entry['top']),
                int(entry['width']),
                int(entry['height']))
            self.stats.append_player(player)

        self.stats.thread_count -= 1

    def __update_players_text(self, frame, count: int):
        frame_height, frame_width, _ = frame.shape
        players = f'Players Observed: {self.stats.get_last_players(count)}'
        position = (10, frame_height - 170)
        font = cv2.QT_FONT_NORMAL
        font_scale = 1
        font_color = (0, 0, 255)
        font_thickness = 3

        cv2.putText(frame, players, position, font, font_scale, font_color, font_thickness)

    def __update_players_rect(self, frame):
        players_positions = self.stats.get_players_position()

        for player_position in players_positions:
            left = player_position[0]
            top = player_position[1]
            width = player_position[2]
            height = player_position[3]

            cv2.rectangle(frame, (left, top), (left + width, top + height), (0, 0, 255), 2)
