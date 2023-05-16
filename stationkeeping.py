import numpy

class control_loop(object):
    def __init__(self, ax0, ay0):
        self.x, self.y = 0, 0
        self.vx, self.vy = 0, 0
        self.ax, self.ay = ax0, ay0

    def update_xy(self, ax_new, ay_new, dt):
        #ax and ay are arrays of the last k inputs
        axi_new = numpy.average(ax_new)
        ayi_new = numpy.average(ay_new)

        print('C ACC OUTPUT' + str(axi_new) + ' ' + str(ayi_new))
        
        #integrate using input & previous cycle input
        vxi_new = self.vx + dt * (axi_new - self.ax)
        vyi_new = self.vy + dt * (ayi_new - self.ay)

        self.x = self.x + dt * (vxi_new - self.vx)
        self.y = self.y + dt * (vyi_new - self.vy)

        #update old v and a with new values
        self.ax, self.ax = axi_new, ayi_new
        self.vx, self.vy = vxi_new, vyi_new

        print('C POS OUTPUT' + str(self.x) + ' ' + str(self.y))

    def PID(self):
        '''
        ERROR: x, y displacement is (0, 0) to (self.x, self.y)
        '''
        errorX = - self.x
        errorY = - self.y

        Kp = 100
        #Kd = 0
        #Ki = 0

        #errorIX = 0l errorIY = 0
        #d_errorX = 0; d_errorY = 0
        #past_errorX = 0; past_errorY = 0

        max_dist = .5

        ''' I and D will not work, variable is only in this frame'''
        #errorIX = errorIX + errorX
        #errorIY = errorIY + errorY

        #d_errorX = (errorX - past_errorX)/delta_t
        #d_errorY = (errorY - past_errorY)/delta_t

        #past_errorX = errorX
        #past_errorY = errorY

        cmdX = Kp * errorX #+ Ki * errorIX + Kd * d_errorX
        cmdY = Kp * errorY #+ Ki * errorIX + Kd * d_errorY

        if cmdX > max_dist: cmdX = max_dist
        if cmdY > max_dist: cmdY = max_dist

        XA = 0 # POINTED IN +x
        XB = 0 # POINTED IN -x
        YA = 0 # POINTED IN +y
        YB = 0 # POINTED IN -y

        # Hypothetical Max = .5m
        # Velocity = distance/time
        
        offset = 400

        '''this does not make sense'''
        if cmdX <= 0:
            XA = 1500 - (offset/max_dist)*cmdX 
            XB = 1500 - (offset/max_dist)*cmdX
        else:
            XA = 1500 + (offset/max_dist)*cmdX
            XB = 1500 + (offset/max_dist)*cmdX

        if cmdY <= 0:
            YA = 1500 - (offset/max_dist)*cmdY
            YB = 1500 - (offset/max_dist)*cmdY
        else:
            YA = 1500 + (offset/max_dist)*cmdY
            YB = 1500 + (offset/max_dist)*cmdY
            
        return [XA, XB, YA, YB]