import src.config as conf

# noinspection PyUnresolvedReferences
import board
# noinspection PyUnresolvedReferences
import neopixel

from src.output.matrix import NeoMatrix

# noinspection PyUnresolvedReferences
import RPi.GPIO as GPIO
import time

import asyncio


class Base:

    def __init__(self):
        # TODO: get Values from Config
        self.wakeupCM = 10

        # TODO: test step count and max
        self.steps = 10
        self.max = 40

        # TODO: set pins corresponding to Hardware (from config)
        self.trigger = 1
        self.echo = 2


        self.__initConf()

        self.width = self.config.get_config()['main']['width']
        self.height = self.config.get_config()['main']['height']

        self.__initBoard()

        self.__initUltrasonic()

        # TODO: catch error
        import src.gameFiles.FlappyBird as game
        self.gameObj = game.FlappyBird(self, self.output)

        # TODO: catch error
        import src.gameFiles.Screensaver as schoner
        self.schonerObj = schoner.Screensaver(self, self.output)

    def __initConf(self):
        self.config = conf.Config()

    def __initBoard(self):
        # TODO: Get raspy gpio pin from config
        strip_lengh = int(self.width) * int(self.height)
        pixels = neopixel.NeoPixel(board.D18, strip_lengh, auto_write=False)

        self.output = NeoMatrix(int(self.width), int(self.height), pixels)

    def __initUltrasonic(self):
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(self.echo, GPIO.IN)
        GPIO.setup(self.trigger, GPIO.OUT)

    def run(self):
        while True:
            schonerTask = asyncio.create_task(self.__schoner())

            while self.getInput() > self.wakeupCM:
                pass

            schonerTask.cancel()

            # TODO: Catch error
            self.gameObj.run()

    async def __schoner(self):
        try:
            pass
            self.schonerObj.run()
        except asyncio.CancelledError:
            pass

    def getInput(self) -> float:
        GPIO.output(self.trigger, True)
        time.sleep(0.00001)  # 10 Mikrosekunden
        GPIO.output(self.trigger, False)

        while GPIO.input(self.echo) == 0:
            pass
        tstart = time.time()

        while GPIO.input(self.echo) == 1:
            pass
        tstop = time.time()

        dist = ((tstop - tstart) * 34300) / 2  # Schallgeschwindigkeit 343 m/s = 34.300 cm/s
                                               # : 2 um nur einfache Wegstrecke zu berechnen

        return dist

    def convertInput(self, dist: float) -> int:
        idist = int(dist)

        out = int((((idist - 1) // self.steps) * self.steps))
        if out > self.max:
            out = self.max
        if out < 1:
            out = 1

        return out
