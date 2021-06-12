import logging
import time

import pygame
import pygame as pg

from app.input_manager import PygameEventQueueHandler
from app.state import StateManager

logger = logging.getLogger(__name__)


class Client(StateManager):
    """ Client class for entire project. Contains the game loop, and contains
    the event_loop which passes events to States as needed.
    """

    def __init__(self, caption):
        """
        :param caption: The window caption to use for the game itself.
        :type caption: str
        :rtype: None
        """
        super(Client, self).__init__()
        # Set up our game's configuration from the prepare module.
        #self.config = prepare.CONFIG

        # INFO: no need to call superclass for now
        self.screen = pg.display.get_surface()
        self.caption = caption

        #self.fps = self.config.fps
        self.fps = 60
        #self.show_fps = self.config.show_fps

        # Set up a variable that will keep track of currently playing music.
        self.current_music = {"status": "stopped", "song": None, "previoussong": None}

        # Set up the command line. This provides a full python shell for
        # troubleshooting. You can view and manipulate any variables in
        # the game.
        #self.exit = False  # Allow exit from the CLI
        #if self.config.cli:
        #    self.cli = cli.CommandLine(self)

        self.input_manager = PygameEventQueueHandler()

    def main(self):
        """ Initiates the main game loop. Since we are using Asteria networking
        to handle network events, we pass this core.session.Client instance to
        networking which in turn executes the "main_loop" method every frame.
        This leaves the networking component responsible for the main loop.

        :rtype: None
        :returns: None

        """
        update = self.update
        draw = self.draw
        screen = self.screen
        flip = pg.display.update
        clock = time.time
        frame_length = (1. / self.fps)
        time_since_draw = 0
        last_update = clock()
        fps_timer = 0
        frames = 0

        while not self.done:
            clock_tick = clock() - last_update
            last_update = clock()
            time_since_draw += clock_tick
            update(clock_tick)
            if time_since_draw >= frame_length:
                time_since_draw -= frame_length
                draw(screen)
                flip()
                frames += 1

            fps_timer, frames = self.handle_fps(clock_tick, fps_timer, frames)
            time.sleep(.01)

    def update(self, time_delta):
        """Main loop for entire game.
        """
        # get all the input waiting for use
        events = self.input_manager.process_events()
        # processes events, collects unused events
        events = list(self.process_events(events))

        # Update the game engine
        self.update_states(time_delta)

    def process_events(self, events):
        """ Process all events for this frame.
        """
        for game_event in events:
            if game_event:
                game_event = self._send_event(game_event)
                if game_event:
                    yield game_event

    def _send_event(self, game_event):
        """ Send event down processing chain
        """
        for state in self.active_states:
            game_event = state.process_event(game_event)
            if game_event is None:
                break
        else:
            pass
        return game_event


    def update_states(self, dt):
        """ Checks if a state is done or has called for a game quit.

        :param dt: Time delta - Amount of time passed since last frame.

        :type dt: Float
        """

        for state in self.active_states:
            state.update(dt)

        current_state = self.current_state

        # handle case where the top state has been dismissed
        if current_state is None:
            self.done = True

        if current_state in self._state_resume_set:
            current_state.resume()
            self._state_resume_set.remove(current_state)

    def draw(self, surface):
        """ Draw all active states

        :type surface: pg.surface.Surface
        """
        to_draw = list()
        full_screen = surface.get_rect()
        for state in self.active_states:
            to_draw.append(state)

            # if this state covers the screen
            # break here so lower screens are not drawn
            if (not state.transparent
                    and state.rect == full_screen
                    and not state.force_draw):
                break

        # draw from bottom up for proper layering
        for state in reversed(to_draw):
            state.draw(surface)

    def handle_fps(self, clock_tick, fps_timer, frames):
        #if self.show_fps:
        if True:
            fps_timer += clock_tick
            if fps_timer >= 1:
                with_fps = "{} - {:.2f} FPS".format(self.caption, frames / fps_timer)
                pg.display.set_caption(with_fps)
                return 0, 0
            return fps_timer, frames
        return 0, 0

