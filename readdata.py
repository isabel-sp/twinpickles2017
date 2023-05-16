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
        self.ax0 = 20
        self.ay0 = 25
        self.acc = {'x': [self.ax0], 'y': [self.ay0]}

    def get_acc(self): return self.acc

    #converts raw IMU data to boat reference frame
    def convert_acc(self, ax, ay):
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
        self.request_message_interval(id, 10)

    def read_imu_data(self):
        if self.master:
            msg = self.master.recv_match()
            if not msg:
                pass
            elif msg.get_type() == 'SCALED_IMU2':
                print('IMU x y z acc', ((float)(msg.to_dict()['xacc'])), ((float)(msg.to_dict()['yacc'])), ((float)(msg.to_dict()['zacc'])))

                if (len(self.acc['x']) > 3):
                    self.acc['x'].pop(0)
                    self.acc['y'].pop(0)
                    # self.acc['z'].pop(0)
                # print(msg.to_dict()['xacc'])
                # print(msg.to_dict()['yacc'])
                acc_x = (float)(msg.to_dict()['xacc'])
                acc_y = (float)(msg.to_dict()['yacc'])
                converted_xy = self.convert_acc(acc_x, acc_y)
                print(converted_xy)
                self.acc['x'].append(converted_xy[0])
                self.acc['y'].append(converted_xy[1])
                # self.acc['z'].append(self.convert_acc((float)(msg.to_dict()['zacc'])))
            # else:
            #     print(msg.to_dict())


if __name__ == "__main__":
    PX = PX_sensors('/dev/ttyUSB1,57600')
    PX.request_messages('SCALED_IMU2')

    while True:
        PX.read_imu_data()
        print(PX.get_acc())