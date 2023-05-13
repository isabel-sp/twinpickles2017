#helper  module imports
import readdata
import pins
import stationkeeping
import thrusterarduino

#library imports
from threading import Thread
from time import sleep

'''
THREADING PERIODS (delay seconds)
'''

input_period = 0.1
data_read_period = 0.25
stationkeep_period = 0.5

'''
THRUSTER CONTROL
'''

#handeled by thrusterarduino.py

# #thruster initialization
# t0 = thrustercontrol.thruster(0)
# t1 = thrustercontrol.thruster(1)
# t2 = thrustercontrol.thruster(2)
# t3 = thrustercontrol.thruster(3)

# def init_thrusters():
#     t0.initialize()
#     t1.initialize()
#     t2.initialize()
#     t3.initialize()

# def set_thurster_power(power_arr):
#     t0.set_power(power_arr[0])
#     t1.set_power(power_arr[1])
#     t2.set_power(power_arr[2])
#     t3.set_power(power_arr[3])

'''
SEDIMENT DEPLOYMENT
'''

#Setup Input-driven States
inp = ""
winch_up = pins.signal_pin(22)
winch_down = pins.signal_pin(27)
relay = pins.signal_pin(24) #1 for stationkeep, 0 for RC
stationkeep_mode = False

def sediment_input():
    global inp
    global stationkeep_mode

    while True:
        sleep(input_period)
        inp = input("type 2 character winch/relay command and press enter at any time \n (Commands: WINCH- up: wu, down: wd, stop: ws; RELAY- stationkeep: rs, navigate: rn) \n")

        if inp == "wu": #RAISE WINCH #(pin 22 HIGH and pin __pwm HIGH)
            winch_up.set(1)
            winch_down.set(0)
        elif inp == "wd": #LOWER WINCH #(pin 27 HIGH and pin __pwm HIGH)
            winch_up.set(0)
            winch_down.set(1)
        elif inp == "ws": #STOP WINCH
            winch_up.set(0)
            winch_down.set(0)
        elif inp == "rs": #RELAY STATIONKEEP
            relay.set(1)
            # init_thrusters()
            stationkeep_mode = True
        elif inp == "rn": #RELAY NAVIGATE
            relay.set(0)
            stationkeep_mode = False
            
        else: print("command not recognized")


'''
PIXHAWK DATA READING
'''

# PX = readdata.PX_data()
# print('setup & connected to PX')
# PX.request_messages()
# print('PX messages requested')

# def px_update_data():
#     while True:
#         PX.update_position()
#         sleep(data_read_period)


'''
STATIONKEEPING CONTROL LOOP
'''

def stationkeep():
    t0 = 1550
    while True:               
        sleep(stationkeep_period)
        if stationkeep_mode:

            print(thrusterarduino.ser)
            
            #make sure thruster is initialized
            if thrusterarduino.ser == None:
                print("serial not initialized? initializing now!")
                thrusterarduino.thruster_write_init() 

            #simulate PID adjusting thruster power
            if t0 >= 1600: t0 = 1500
            else: t0 = t0 + 25
            print('incremented t0')

            '''
            USING PIXHAWK DATA (OLD VERSION)
            '''
            # # print(PX.get_x(), PX.get_y())
            # thruster_set = stationkeeping.PID(PX.get_x(), PX.get_y())
            # set_thurster_power(thruster_set)
            # # print(power_arr)
            # print(PX.get_dxyz())

            thrusterarduino.thruster_write_power([t0, 1500, 1500, 1500])
            thrusterarduino.thruster_set_power()
            print('stationkeeping!')

        #turn off serial if not stationkeeping   
        else:
            if not thrusterarduino.ser == None: 
                thrusterarduino.thruster_write_stop()



'''
THREADS
'''

t_sediment = Thread(target=sediment_input)
# t_px = Thread(target=px_update_data)
t_stationkeep = Thread(target=stationkeep)

t_sediment.start()
# t_px.start()
t_stationkeep.start()
