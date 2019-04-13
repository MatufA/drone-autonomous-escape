"""
tellopy sample using keyboard and video player

Requires mplayer to record/save video.


Controls:
- tab to lift off
- WASD to move the drone
- space/shift to ascend/descent slowly
- Q/E to yaw slowly
- arrow keys to ascend, descend, or yaw quickly
- backspace to land, or P to palm-land
- enter to take a picture
- R to start recording video, R again to stop recording
  (video and photos will be saved to a timestamped file in ~/Pictures/)
- Z to toggle camera zoom state
  (zoomed-in widescreen or high FOV 4:3)
"""
import threading
import time
import pygame
import pygame.display
import pygame.key
import pygame.locals
import pygame.font


class KeyboardFly(object):

    def __init__(self, drone):
        self.drone = drone
        pygame.font.init()

        self.font = pygame.font.SysFont("dejavusansmono", 32)

        self.hud = [
            FlightDataDisplay('height', 'ALT %3d'),
            FlightDataDisplay('ground_speed', 'SPD %3d'),
            FlightDataDisplay('battery_percentage', 'BAT %3d%%'),
            FlightDataDisplay('wifi_strength', 'NET %3d%%'),
        ]
        self.controls = {
            'w': 'forward',
            's': 'backward',
            'a': 'left',
            'd': 'right',
            'space': 'up',
            'left shift': 'down',
            'right shift': 'down',
            'q': 'counter_clockwise',
            'e': 'clockwise',
            # arrow keys for fast turns and altitude adjustments
            'left': lambda drone, speed: drone.counter_clockwise(speed * 2),
            'right': lambda drone, speed: drone.clockwise(speed * 2),
            'up': lambda drone, speed: drone.up(speed * 2),
            'down': lambda drone, speed: drone.down(speed * 2),
            'tab': lambda drone, speed: drone.takeoff(),
            'backspace': lambda drone, speed: drone.land(),

        }
        self.controller_on = False
        self.was_on = False
        self.my_text = "key control"

    def start_control(self):
        if self.controller_on: return
        self.controller_on = True
        if self.was_on: return
        threading.Thread(target=self.main).start()

    def end_control(self):
        self.controller_on = False

    def flight_data_mode(self, drone, *args):
        return drone.zoom and "VID" or "PIC"

    def update_hud(self, hud, drone, flight_data):
        # width available on side of screen in 4:3 mode
        (w, h) = (158, 0)
        blits = []
        for element in hud:
            surface = element.update(drone, flight_data)
            if surface is None:
                continue
            blits += [(surface, (0, h))]
            # w = max(w, surface.get_width())
            h += surface.get_height()
        # add some padding
        h += 64
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        # remove for mplayer overlay mode
        overlay.fill((0, 0, 0))
        for blit in blits:
            overlay.blit(*blit)
        pygame.display.get_surface().blit(overlay, (0, 0))
        pygame.display.update(overlay.get_rect())

    def status_print(self, text):
        pygame.display.set_caption(text)

    def flightDataHandler(self, event, sender, data):
        global prev_flight_data
        text = str(data)
        if prev_flight_data != text:
            self.update_hud(self.hud, sender, data)
            prev_flight_data = text

    def set_text(self, txt):
        self.my_text = txt

    def disp_text(self, txt):
        # Fill background
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((250, 250, 250))

        # Display some text
        text = self.font.render(txt, 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        background.blit(text, textpos)

        # Blit everything to the screen
        self.screen.blit(background, (0, 0))
        pygame.display.flip()

    def main(self):
        pygame.init()
        pygame.font.init()  # you have to call this at the start,
        pygame.display.init()
        self.screen = pygame.display.set_mode((400, 300))

        self.font = pygame.font.SysFont("dejavusansmono", 32)

        self.was_on = True
        speed = 30

        while True:
            self.disp_text(self.my_text)
            time.sleep(0.01)  # loop with pygame.event.get() is too mush tight w/o some sleep
            for e in pygame.event.get():
                if self.controller_on:
                    # WASD for movement
                    if e.type == pygame.locals.KEYDOWN:
                        keyname = pygame.key.name(e.key)
                        if keyname == 'escape':
                            self.end_control()
                        if keyname in self.controls:
                            key_handler = self.controls[keyname]
                            if type(key_handler) == str:
                                getattr(self.drone, key_handler)(speed)
                            else:
                                key_handler(self.drone, speed)

                    elif e.type == pygame.locals.KEYUP:
                        keyname = pygame.key.name(e.key)
                        if keyname in self.controls:
                            key_handler = self.controls[keyname]
                            if type(key_handler) == str:
                                getattr(self.drone, key_handler)(0)
                            else:
                                key_handler(self.drone, 0)


class FlightDataDisplay(object):
    # previous flight data value and surface to overlay
    _value = None
    _surface = None
    # function (drone, data) => new value
    # default is lambda drone,data: getattr(data, self._key)
    _update = None

    def __init__(self, key, format, colour=(255, 255, 255), update=None):
        self._key = key
        self._format = format
        self._colour = colour

        if update:
            self._update = update
        else:
            self._update = lambda drone, data: getattr(data, self._key)

    def update(self, drone, data):
        new_value = self._update(drone, data)
        if self._value != new_value:
            self._value = new_value
            self._surface = self.font.render(self._format % (new_value,), True, self._colour)
        return self._surface
