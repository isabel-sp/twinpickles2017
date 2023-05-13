import board
import busio
import adafruit_pca9685
import time

i2c = busio.I2C(board.SCL, board.SDA)
hat = adafruit_pca9685.PCA9685(i2c)
hat.frequency = 47

#DUTY CYCLE FORUMLA
#(1/f) [period] * (dutycycle/65535) [on %] = 1500 microseconds

#range is 1100 to 1900
#values tend to be -100 ms off
high = 1900
low = 1100
#1500, but adjusted for -100 off
zero = 1600 

t0 = hat.channels[0]
t1 = hat.channels[1]
t2 = hat.channels[2]
t3 = hat.channels[3]

#initialize


#zero signal to arm thruster
thruster_channel0.duty_cycle = int((zero/1000000) * hat.frequency * 65535)
time.sleep(2)

while True:
    thruster_channel0.duty_cycle = int((1800/1000000) * hat.frequency * 65535)
    time.sleep(2)
    thruster_channel0.duty_cycle = int(((zero)/1000000) * hat.frequency * 65535)
    # thruster_channel1.duty_cycle = int((low/1000000) * hat.frequency * 65535)
    time.sleep(2)






