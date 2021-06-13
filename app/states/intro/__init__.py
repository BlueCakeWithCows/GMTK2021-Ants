import os.path
import app.asset_manager
from app.input_manager import Button
from app.state import State
from pygame import mixer
import time


class IntroState(State):
    def process_event(self, event):
        if event.button == Button.QUIT or (event.button == Button.ESCAPE and event.pressed):
            self.client.done = True
            menu_shutdown_music = app.asset_manager.load_audio(os.path.join("assets", "menu_shutdown.mp3"))
            mixer.music.stop()
            menu_shutdown_music.play()
            time.sleep(2)

        if event.button == Button.INTERACT:
            menu_music = app.asset_manager.load_audio(os.path.join("assets", "menu_click.mp3"))
            menu_music.play()
            time.sleep(.7)
            self.client.push_state("MenuState")
            self.client.pop_state("WorldState")

    def update(self, time_delta):  # this is for updating objects, updating keystrokes, whateva
        self.animations.update(time_delta)  # lmao what is this?

    def draw(self, surface):  # draw shit on surface after startup, main loop will render this automatically
        menu_img = app.asset_manager.load_image(os.path.join("assets", "Splash.png"))
        surface.blit(menu_img, (0, 0))

    def startup(self, **kwargs):  # when it's pushed for the first time, initializes things
        mixer.init()
        mixer.music.load(os.path.join("assets", "menu_music.mp3"))
        mixer.music.set_volume(0.5)
        mixer.music.play(loops=-1)

    def resume(self):
        pass

    def pause(self):
        pass

    def cleanup(self):
        pass
