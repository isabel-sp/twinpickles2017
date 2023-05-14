#helper  module imports
import readdata
import pins
import stationkeeping
import thrusterarduino

#library imports
from threading import Thread
from time import sleep

thruster_arduino_port = '/dev/ttyACM0'
pixhawk_port = '/dev/ttyUSB0,57600'

'''
THREADING PERIODS (delay seconds)
'''

input_period = 0.1
data_read_period = 0.1
stationkeep_period = 0.25

'''
STATES & INPUTS
'''

#Setup Input-driven States
inp = ""
stationkeep_mode = False
winch_up = pins.signal_pin(22) #HIGH (3.3v) for up
winch_down = pins.signal_pin(27) #LOW (3.3v) for down
relay = pins.signal_pin(24) #1 for stationkeep, 0 for RC


def state_input():
    global inp
    global stationkeep_mode

    while True:
        sleep(input_period)
        inp = input("type command and press enter \n (Commands: WINCH (up: wu, down: wd, stop: ws) MODE (stationkeep: rs, navigate: rn) \n")

        if inp == "wu": #RAISE WINCH #(pin 22 HIGH and pin __pwm HIGH)
            winch_up.set(1)
            winch_down.set(0)
        elif inp == "wd": #LOWER WINCH #(pin 27 HIGH and pin __pwm HIGH)
            winch_up.set(0)
            winch_down.set(1)
        elif inp == "ws" or inp == " ": #STOP WINCH
            winch_up.set(0)
            winch_down.set(0)
        elif inp == "rs": #RELAY STATIONKEEP
            relay.set(1)
            # init_thrusters()
            stationkeep_mode = True
        elif inp == "rn": #RELAY NAVIGATE
            relay.set(0)
            stationkeep_mode = False
        elif inp == "hi":
            print("hello!")
            
        else: print("command not recognized")


'''
PIXHAWK DATA READING
'''
try:
    PX = readdata.PX_sensors(pixhawk_port)
    print('connected to PX')
    PX.request_messages()
    print('PX messages requested')
except:
    PX = None
    print('PX connection failed. rerun code to try again')

def px_update_data():
    while not PX == None:
        PX.read_imu_data()
        sleep(data_read_period)


'''
STATIONKEEPING CONTROL LOOP
'''
def stationkeep():
    while True:               
        sleep(stationkeep_period)

        if stationkeep_mode and not PX == None:
            #INITIALIZE THRUSTER COMMUNICATION
            #INITIALIZE CONTROL LOOP
            if thrusterarduino.ser == None:
                print("serial not initialized? initializing now!")
                thrusterarduino.thruster_write_init(thruster_arduino_port)

            if controller == None: 
                print("starting controller now!")
                controller = stationkeeping.control_loop(PX.ax0, PX.ay0)

            #INTEGRATES IMU DATA
            controller.updatexy(PX.get_ax(), PX.get_ay(), stationkeep_period)

            #CALCULATE THRUSTER SPEED
            thruster_speeds = controller.PID()
            print("THRUSTER SPEEDS" + str(thruster_speeds))

            #WRITE POWER
            thrusterarduino.thruster_write_speed(thruster_speeds)
            #SEND POWER OVER SERIAL
            thrusterarduino.thruster_send_speed()

        #not stationkeeping mode
        else: 
            #reset controller
            controller = None
            #turn off serial
            if not thrusterarduino.ser == None: 
                thrusterarduino.thruster_write_stop()

'''
THREADS
'''

t_state = Thread(target=state_input)
t_px = Thread(target=px_update_data)
t_stationkeep = Thread(target=stationkeep)

t_state.start()
t_px.start()
t_stationkeep.start()
