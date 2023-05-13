'''
OLD - FOR SERVOHAT
'''
#Function Definition for Thurster Control
import board
import busio
import adafruit_pca9685
import time

i2c = busio.I2C(board.SCL, board.SDA)
hat = adafruit_pca9685.PCA9685(i2c)
hat.frequency = 47

#(1/f) [period] * (dutycycle/65535) [on %] = 1500 microseconds

#range is 1100 to 1900, values tend to be -100 us off
high = 1900
low = 1100
#should be 1500, but adjusted for -100 off
zero = 1600


def microseconds_to_dutycycle(ms):
    return int((ms/1000000) * hat.frequency * 65535)

# def set_ms(channel, ms):
#     hat.channels[channel] = (int) (microseconds_to_dutycycle(ms))
#     print(str(channel) + " set to" + str(ms))

# def set_power(channel, power):
#     set_ms(channel, (int)(low + power*(high-low)))

# def sweep(channel):
#     for ms in range(low, high, 25):
#         set_ms(channel, ms)
#         time.sleep(0.05)
#     for ms in range(high, low, -25):
#         set_ms(channel, ms)
#         time.sleep(0.05)
#     #end sweep at 0
#     set_ms(channel, zero)

# t0 = hat.channels[0]
# t1 = hat.channels[1]
# t2 = hat.channels[2]
# t3 = hat.channels[3]

class thruster(object):
    def __init__(self, channel):
        self.channel = channel
        print("INIT THRUSTER " + str(channel))
    
    def initialize(self):
        self.sweep(zero-50, zero+50)
        print("SWEEP THRUSTER " + str(self.channel))
    
    def set_ms(self, ms):
        hat.channels[self.channel].duty_cycle = ((int) (microseconds_to_dutycycle(ms)))
        # print(str(self.channel) + " set to " + str(ms)+"ms")
    
    def set_power(self, power):
        self.set_ms((int)(low + power*(high-low)))
    
    def sweep(self, l, h):
        for ms in range(l, h, 25):
            self.set_ms(ms)
            time.sleep(0.05)
        for ms in range(h, l, -25):
            self.set_ms(ms)
            time.sleep(0.05)
        #end sweep at 0
        self.set_ms(zero)
