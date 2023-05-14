"""
Connect to Pixhawk and request messages
"""

# Import mavutil
from pymavlink import mavutil
import math



class PX_sensors(object):
    def __init__(self, port):
        self.master = mavutil.mavlink_connection(port)
        # self.master.reboot_autopilot()

        #NEED TO ADD: CALIBRATION MEASUREMENTS
        self.ax0 = 0
        self.ay0 = 40
        self.acc = {'x': [self.ax0], 'y': [self.ay0]}

    def get_acc(self): return self.acc

    #converts raw IMU data to boat reference frame
    def convert_acc(ax, ay):
        c = math.sqrt(2)/2
        return [c*ax + c*ay, -c*ax + c*ay]

    def request_message_interval(self, message_input: str, frequency_hz: float):
        message_name = "MAVLINK_MSG_ID_" + message_input
        message_id = getattr(mavutil.mavlink, message_name)
        self.master.mav.command_long_send(
            self.master.target_system, self.master.target_component,
            mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0,
            message_id, 1e6 / frequency_hz, 0, 0, 0, 0, 0)
        print("Requested the message successfully.")
    
    def request_messages(self, id):
        self.request_message_interval(self.master, id, 10)

    def read_imu_data(self):
        if self.master:
            msg = self.master.recv_match()
            if not msg:
                pass
            elif msg.get_type() == 'SCALED_IMU3':
                print('IMU x y z acc', ((float)(msg.to_dict()['xacc'])), ((float)(msg.to_dict()['yacc'])), ((float)(msg.to_dict()['zacc'])))

                if (len(self.acc['x']) > 3):
                    self.acc['x'].pop(0)
                    self.acc['y'].pop(0)
                    # self.acc['z'].pop(0)
                    
                self.acc['x'].append(self.convert_acc((float)(msg.to_dict()['xacc'])))
                self.acc['y'].append(self.convert_acc((float)(msg.to_dict()['yacc'])))
                # self.acc['z'].append(self.convert_acc((float)(msg.to_dict()['zacc'])))


if __name__ == "__main__":
    PX = PX_sensors()
    PX.request_messages('SCALED_IMU2')

    while True:
        PX.read_imu_data()
        print(PX.get_acc())