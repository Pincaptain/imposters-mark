import sys

import numpy
import cv2
from PIL import ImageGrab

from imposters_mark.repositories.window_repository import WindowRepository

ESCAPE_KEY = 27


# noinspection PyUnusedLocal
def t_main(argv):
    pass


# noinspection PyUnusedLocal
def main(argv):
    window_repository = WindowRepository()
    window_rect = window_repository.get_window_rect('Among Us')

    while True:
        image = ImageGrab.grab(bbox=window_rect)
        image_array = numpy.array(image)
        image_frame = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)

        cv2.imshow('Screen', image_frame)

        if cv2.waitKey(1) == ESCAPE_KEY:
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv)
