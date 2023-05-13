import readdata
import pins

from threading import Timer
from time import sleep

#THRUSTER CONTROL
# import board
# import busio
# import adafruit_pca9685
# i2c = busio.I2C(board.SCL, board.SDA)
# hat = adafruit_pca9685.PCA9685(i2c)
# hat.frequency = 47
# #range is 1100 to 1900, values tend to be -100 ms off
# high = 1900
# low = 1100
# zero = 1600
# thruster_channel0 = hat.channels[0]
# #zero signal to arm thruster
# thruster_channel0.duty_cycle = int((zero/1000000) * hat.frequency * 65535)


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

# #THRUSTER SETUP
# t1 = thrustercontrol.Thruster(0)

#PIN SETUP
winch_up = pins.signal_pin(22)
winch_down = pins.signal_pin(27)
i = "no input"

#PX SETUP
PX = readdata.PX_data()
print('setup PX')
PX.request_messages()
print('PX messages requested')
print ("starting timer")

#PX data output
rt = RepeatedTimer(2, PX.get_x)

while True:
    #PX recieve message if there is one
    PX.update_position()

    i = input("")

    if i == "u": #RAISE WINCH
        winch_up.set(1)
        winch_down.set(0)
    if i == "d": #LOWER WINCH
        winch_up.set(0)
        winch_down.set(1)
    if i == "s": #STOP WINCH
        winch_up.set(0)
        winch_down.set(0)
    
