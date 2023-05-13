"""
Connect to Pixhawk and request messages
"""

# Import mavutil
from pymavlink import mavutil
import numpy

def request_message_interval(master, message_input: str, frequency_hz: float):
    message_name = "MAVLINK_MSG_ID_" + message_input
    message_id = getattr(mavutil.mavlink, message_name)
    master.mav.command_long_send(
        master.target_system, master.target_component,
        mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0,
        message_id, 1e6 / frequency_hz, 0, 0, 0, 0, 0)
    print("Requested the message successfully.")


class PX_data(object):
    def __init__(self, x = 0.0, y = 0.0):
        self.master = mavutil.mavlink_connection('/dev/ttyUSB0,57600')
        # self.master.reboot_autopilot()
        self.x = x
        self.y = y

        self.acc = {'x': [0], 'y': [0], 'z': [0]}

    
    def get_x(self): return self.x
    def get_y(self): return self.y
    def get_acc(self): return self.acc

    # def displacement_xyz(self):
    #     return [dx, dy, dz]

    # def mini_integrate(self, L, dt):
    #     return [(L[i] - L[i-1])*dt for i in range(1, len(L))]

    # def get_acc_avg(self, i = 10, end = 0): 
    #     # return self.acc['x']
    #     l = len(self.acc['x'])
    #     if l < i: return None
    #     return {'x': numpy.average(self.acc['x'][l-end-i: l-end]), 'y': numpy.average(self.acc['y'][l-end-i: l-end]), 'z': numpy.average(self.acc['z'][l-end-i: l-end])}
    
    # def get_dxyz(self, dt = 0.25, moving_avg_a = 3, ai = 3):
    #     print("CALLING ON ", self.acc)
    #     a_avg_x = []
    #     a_avg_y = []
    #     a_avg_z = []
    #     #moving average of acceleration values
    #     for i in range(ai):
    #         ai_avg = self.get_acc_avg(moving_avg_a, i*moving_avg_a)
    #         if not ai_avg: return None
    #         a_avg_x.append(ai_avg['x'])
    #         a_avg_y.append(ai_avg['y'])
    #         a_avg_z.append(ai_avg['z'])
    #     print(a_avg_x)
    #     print(a_avg_y)
    #     print(a_avg_z)
    #     #get set of velocity values
    #     v_avg_x = self.mini_integrate(a_avg_x, moving_avg_a*dt)
    #     v_avg_y = self.mini_integrate(a_avg_y, moving_avg_a*dt)
    #     v_avg_z = self.mini_integrate(a_avg_z, moving_avg_a*dt)
    #     print(v_avg_x)
    #     print(v_avg_y)
    #     print(v_avg_z)
    #     #get displacements
    #     d_x = sum(self.mini_integrate(v_avg_x, moving_avg_a*dt))
    #     d_y = sum(self.mini_integrate(v_avg_y, moving_avg_a*dt))
    #     d_z = sum(self.mini_integrate(v_avg_z, moving_avg_a*dt))
    #     return [d_x, d_y, d_z]

    def request_message_interval(self, message_input: str, frequency_hz: float):
        message_name = "MAVLINK_MSG_ID_" + message_input
        message_id = getattr(mavutil.mavlink, message_name)
        self.master.mav.command_long_send(
            self.master.target_system, self.master.target_component,
            mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0,
            message_id, 1e6 / frequency_hz, 0, 0, 0, 0, 0)
        print("Requested the message successfully.")
    
    # def request_messages(self):
    #     request_message_interval(self.master, 'LOCAL_POSITION_NED', 2)
    
    def request_messages_custom(self, id):
        request_message_interval(self.master, id, 5)
    
    def update_position(self):
        if self.master:
            msg = self.master.recv_match()
            if not msg:
                pass
            # elif msg.get_type() == 'LOCAL_POSITION_NED':
            #     pass
            #     self.x = (float)(msg.to_dict()['x'])
            #     self.y = (float)(msg.to_dict()['y'])
            #     print('LOCAL_POSITION_NED X Y', ((float)(msg.to_dict()['x'])), ((float)(msg.to_dict()['y'])))
            #     print('LOCAL_POSITION_NED VX VY', ((float)(msg.to_dict()['vx'])), ((float)(msg.to_dict()['vy'])))
            elif msg.get_type() == 'SCALED_IMU3':
                # print(msg.to_dict())
                print('IMU x y z acc', ((float)(msg.to_dict()['xacc'])), ((float)(msg.to_dict()['yacc'])), ((float)(msg.to_dict()['zacc'])))
                if (len(self.acc['x']) > 10):
                    self.acc['x'].pop(0)
                    self.acc['y'].pop(0)
                    self.acc['z'].pop(0)
                    
                self.acc['x'].append((float)(msg.to_dict()['xacc']))
                self.acc['y'].append((float)(msg.to_dict()['yacc']))
                self.acc['z'].append((float)(msg.to_dict()['zacc']))






if __name__ == "__main__":
    PX = PX_data()
    # PX.request_messages()
    # PX.request_messages_custom('HIGHRES_IMU')
    PX.request_messages_custom('SCALED_IMU2')

    while True:
        PX.update_position()
        # print(PX.get_x())