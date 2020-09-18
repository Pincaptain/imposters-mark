import sys

import cv2

from imposters_mark.configs.injection_config import InjectionConfig

ESCAPE_KEY = 27


# noinspection PyUnusedLocal
def t_main(argv):
    pass


# noinspection PyUnusedLocal
def main(argv):
    injection_config = InjectionConfig()
    screen_service = injection_config.get_screen_service()

    while True:
        screen = screen_service.get_screen('Among Us')

        cv2.namedWindow('Screen', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('Screen', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow('Screen', screen)

        if cv2.waitKey(1) == ESCAPE_KEY:
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv)
