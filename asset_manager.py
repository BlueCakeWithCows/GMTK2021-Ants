import pygame
import logging

import prepare
from pygame import mixer

logger = logging.getLogger(__name__)


def transform_resource_filename(*filename):
    """ Appends the resource folder name to a filename
    :param filename: String
    :rtype: basestring
    """
    return prepare.fetch(*filename)


def load_image(filename):
    """ Load image from the resources folder
    """

    filename = transform_resource_filename(filename)
    return pygame.image.load(filename)


class DummySound:
    def play(self):
        pass


def load_audio(filename):
    """ Load sound from the resources folder
    """
    filename = transform_resource_filename(filename)
    try:
        return mixer.Sound(filename)
    except pygame.error as e:
        logger.error(e)
        logger.error('Unable to load sound: {}'.format(filename))
        return DummySound()
