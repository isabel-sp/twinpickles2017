import numpy as np
import matplotlib.pyplot as plt
import readdata
import time



if __name__ == "__main__":

    '''
    test to print imu data to graph
    '''
    
    PX = readdata.PX_data()
    PX.request_messages_custom('SCALED_IMU2')

    start = time.time()
    while (time.time() - start < 2):
        PX.update_position()
    
    a = PX.get_acc()
    print(a)
    print(PX.get_acc_avg())
    axis = [i for i in range(0, len(a['x']))]

    # plt.plot(axis, a['x'])
    # plt.plot(axis, a['y'])
    # plt.plot(axis, a['z'])
    # plt.savefig('/home/tim/Desktop/twinpickles/graph.png')