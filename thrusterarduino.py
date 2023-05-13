#!/usr/bin/env python3

import serial # Module needed for serial communication
import time # Module needed to add delays in the code

#initialize serial
ser = None

#initialize thruster power to 0
thruster_power = [1500, 1500, 1500, 1500]


'''
SETUP THRUSTER COMMUNICATION
run everytime stationkeeping mode is entered
'''
def thruster_write_init():
  global ser

  try:
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()
  except: 
    ser = None
    print("error connecting to arduino :()")
  
  if not ser == None:
    print("arduino (should be?) initializing")
    time.sleep(15)
    print("SENDING FIRST COMMANDS")
  
    zero = ("1500, 1500, 1500, 1500" +"\n")
    slow = ("1525, 1525, 1525, 1525" +"\n")

    #try sending first 3 commands to serial!
    try:
      ser.write(zero.encode('utf-8'))
      time.sleep(1)
      ser.write(slow.encode('utf-8'))
      time.sleep(1)
      ser.write(zero.encode('utf-8'))
      time.sleep(1)
      print("SERIAL IS GOOD YAY")
    except: print("error writing to arduino :(")

def thruster_write_power(values):
  #convert PID output into values
  global thruster_power
  thruster_power = values

def thruster_set_power():
  global ser
  send_string = (str(thruster_power[0]) + ", " + str(thruster_power[1]) + ", "  + str(thruster_power[2]) + ", "  + str(thruster_power[3]) +"\n")
  print("sending string now: " + send_string)

  try:
    ser.write(send_string.encode('utf-8'))
  except: print("error writing to arduino :(")
  
  #RECIEVE DATA FROM ARDUINO SERIAL MONITOR
  #(causes big delay)
  # try:
  #   receive_string = ser.readline().decode('utf-8').rstrip()
  #   print(receive_string)
  # except: pass
    
def thruster_reset():
  #directly reset power
  global thruster_power
  thruster_power = [1500, 1500, 1500, 1500]
  thruster_set_power()

def thruster_write_stop():
  global ser
  thruster_reset()
  ser = None


if __name__ == "__main__":

  ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
  ser.flush()

  t0 = 1500

  print("INITIALIZING")
  time.sleep(15)

  print("SENDING COMMANDS")
  while (1):
    
    #sweep
    if t0 >= 1600: t0 = 1500
    else: t0 = t0 + 25

    values = [t0, 1550, 1550, 1550]
    send_string = (str(values[0]) + ", " + str(values[1]) + ", "  + str(values[2]) + ", "  + str(values[3]) +"\n")
    print("sending string now: " + send_string)
    
    # Send the string. Make sure you encode it before you send it to the Arduino.
    try:
      ser.write(send_string.encode('utf-8'))
    except: print("error writing to arduino :(")
    
    # Do nothing for 500 milliseconds (0.5 seconds)
    time.sleep(0.1)
  
    # Receive data from the Arduino and print
    # try:
    #   receive_string = ser.readline().decode('utf-8').rstrip()
    #   print(receive_string)
    # except: pass