import sys

import cv2

from imposters_mark.configs.injection_config import InjectionConfig
from imposters_mark.entities.stats import Stats

ESCAPE_KEY = 27


# noinspection PyUnusedLocal
def t_main(argv):
    stats = Stats()
    stats.append_location('Admin')
    stats.append_location('Reactor')
    stats.append_location('Cafe')
    print(stats.get_current_location())
    print(stats.get_last_locations(110))


# noinspection PyUnusedLocal
def main(argv):
    injection_config = InjectionConfig('../resources/config.ini')
    game_service = injection_config.get_game_service()

    while True:
        frame = game_service.update()

        cv2.namedWindow('Screen', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('Screen', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow('Screen', frame)

        if cv2.waitKey(1) == ESCAPE_KEY:
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv)
