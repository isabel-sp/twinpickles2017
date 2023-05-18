import numpy

class control_loop(object):
    def __init__(self, ax_new, ay_new):
        self.x, self.y = 0, 0
        self.vx, self.vy = 0, 0
        self.ax, self.ay = 0, 0
        self.ax0, self.ay0 = numpy.average(ax_new), numpy.average(ay_new)

        # self.errord_x = 0
        # self.errord_y = 0

    def update_xy(self, ax_new, ay_new, dt):
        #ax and ay are arrays of the last k inputs
        axi_new = numpy.average(ax_new)
        ayi_new = numpy.average(ay_new)

        print('IMU ACC OUTPUT SCALED: ' + str(axi_new) + ' ' + str(ayi_new))
        
        # #integrate using input & previous cycle input
        # vxi_new =  self.vx + dt * (axi_new)
        # vyi_new = self.vy + dt * (ayi_new)

        # self.x = self.x + dt * (vxi_new)
        # self.y = self.y + dt * (vyi_new)

        # #update old v and a with new values
        self.ax, self.ay = axi_new, ayi_new
        # self.vx, self.vy = vxi_new, vyi_new

        # print('CONTROLLER POS INPUT: ' + str(self.x) + ' ' + str(self.y))

    def PID(self):
        '''
        ERROR: x, y displacement is (0, 0) to (self.x, self.y)
        '''
        errorX = - self.ax
        errorY = - self.ay

        Kp = 0.05
        Kd = 0
        #Ki = 0

        #errorIX = 0l errorIY = 0

        '''past_errorX = 0; past_errorY = 0'''

        max_dist = .5

        ''' I and D will not work, variable is only in this frame'''
        #errorIX = errorIX + errorX
        #errorIY = errorIY + errorY
        """
        self.errord_x = (errorX - past_errorX)/self.dt
        self.errord_y = (errorY - past_errorY)/self.dt
        
        past_errorX = errorX
        past_errorY = errorY
        """
        cmdX = Kp * errorX #+ #Kd * self.errord_x # Ki*errorIX
        cmdY = Kp * errorY #+ #Kd * self.errord_y # Ki* errorIX
        if (cmdX > max_dist): cmdX = max_dist
        if (cmdY > max_dist): cmdY = max_dist
        if (cmdX < -max_dist): cmdX = -max_dist
        if (cmdY < -max_dist): cmdY = -max_dist

        XA = 0 # POINTED IN +x
        XB = 0 # POINTED IN -x
        YA = 0 # POINTED IN +y
        YB = 0 # POINTED IN -y

        # Hypothetical Max = .5m
        # Velocity = distance/time
        
        offset = 125

        '''this does not make sense'''
        if cmdX <= 0:
            XA = 1500 - (offset/max_dist)*cmdX 
            XB = 1500 + (offset/max_dist)*cmdX
        else:
            XA = 1500 + (offset/max_dist)*cmdX
            XB = 1500 - (offset/max_dist)*cmdX

        if cmdY <= 0:
            YA = 1500 - (offset/max_dist)*cmdY
            YB = 1500 + (offset/max_dist)*cmdY
        else:
            YA = 1500 + (offset/max_dist)*cmdY
            YB = 1500 - (offset/max_dist)*cmdY
            
        return [XA, XB, YA, YB]