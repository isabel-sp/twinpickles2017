"""
Example of how to filter for specific mavlink messages coming from the
autopilot using pymavlink.

Can also filter within recv_match command - see "Read all parameters" example
"""
#https://www.ardusub.com/developers/pymavlink.html#read-all-parameters


# Import mavutil
from pymavlink import mavutil

# Create the connection
# From topside computer
master = mavutil.mavlink_connection('/dev/ttyUSB0,57600')
# master.reboot_autopilot()


def request_message_interval(master, message_input: str, frequency_hz: float):
    message_name = "MAVLINK_MSG_ID_" + message_input
    message_id = getattr(mavutil.mavlink, message_name)
    master.mav.command_long_send(
        master.target_system, master.target_component,
        mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0,
        message_id, 1e6 / frequency_hz, 0, 0, 0, 0, 0)
    print("Requested the message successfully.")

request_message_interval(master, 'GLOBAL_POSITION_INT', 2)
request_message_interval(master, 'LOCAL_POSITION_NED', 2)
request_message_interval(master, 'CONTROL_SYSTEM_STATE', 2)


while True:
    msg = master.recv_match()
    if not msg:
        continue
    # elif msg.get_type() == 'HEARTBEAT':
        print("\n\n*****Got message: %s*****" % msg.get_type())
        # print("Message: %s" % msg)
        print("\nAs dictionary: %s" % msg.to_dict())
        # Armed = MAV_STATE_STANDBY (4), Disarmed = MAV_STATE_ACTIVE (3)
        # print("\nSystem status: %s" % msg.system_status)
    # elif msg.get_type() == 'GLOBAL_POSITION_INT':
        # print("\n\n*****Got message: %s*****" % msg.get_type())
        # print("\nAs dictionary: %s" % msg.to_dict())
        print('GLOBAL_POSITION_INT', ((int)(msg.to_dict()['lat']))/10000000, ((int)(msg.to_dict()['lon']))/10000000)
    elif msg.get_type() == 'LOCAL_POSITION_NED':
        # x = (float)(msg.to_dict()['x'])
        # y = (float)(msg.to_dict()['y'])
        # z = (float)(msg.to_dict()['z'])
        print('LOCAL_POSITION_NED', ((float)(msg.to_dict()['x'])), ((float)(msg.to_dict()['y'])))
    elif msg.get_type() == 'CONTROL_SYSTEM_STATE':
        # x = (float)(msg.to_dict()['x'])
        # y = (float)(msg.to_dict()['y'])
        # z = (float)(msg.to_dict()['z'])
        print(msg)

    # else:
        # print("\n\n*****Got message: %s*****" % msg.get_type())
        # print("\nAs dictionary: %s" % msg.to_dict())