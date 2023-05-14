import numpy



class control_loop(object):
    def __init__(self, ax0, ay0):
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.ax = ax0
        self.ay = ay0

    def update_xy(self, axi_new, ayi_new, dt):
        #ax and ay are arrays of the last k inputs
        axi = numpy.average(axi_new)
        ayi = numpy.average(ayi_new)
        
        #integrate
        vxi = self.vx + dt * (axi - self.ax)
        vyi = self.vy + dt * (ayi - self.ay)

        self.x = self.x + dt * (vxi - self.vx)
        self.y = self.y + dt * (vyi - self.vy)

        #update old v and a with new values
        self.ax = axi
        self.ay = ayi
        self.vx = vxi
        self.vy = vyi

    def PID(self):

        x_displacement = self.x
        y_displacement = self.y

        Kp = 0
        #Kd = 0
        #Ki = 0

        #errorIX = 0
        #errorIY = 0

        #d_errorX = 0
        #d_errorY = 0

        #past_errorX = 0
        #past_errorY = 0

        #delta_t = 0

        max_dist = .5

        currentX = x_displacement
        currentY = y_displacement
        # Implement moving average
        errorX = 0 - currentX
        errorY = 0 - currentY

        #errorIX = errorIX + errorX
        #errorIY = errorIY + errorY

        #d_errorX = (errorX - past_errorX)/delta_t
        #d_errorY = (errorY - past_errorY)/delta_t

        #past_errorX = errorX
        #past_errorY = errorY

        cmdX = Kp * errorX #+ Ki * errorIX + Kd * d_errorX
        cmdY = Kp * errorY #+ Ki * errorIX + Kd * d_errorY

        percent1 = 0 # x1
        percent2 = 0 # x2
        percent3 = 0 # y1
        percent4 = 0 # y2
        # Hypothetical Max = .5m
        # Velocity = distance/time
        offset = 400

        if cmdX <= 0:
            #send to x1 motor
            percent1 = 1500 - 400*cmdX/max_dist 
            percent2 = 1500 - 400*cmdX/max_dist

        else:
            #send to x2 motor
            percent1 = 1500 + 400*cmdX/max_dist
            percent2 = 1500 + 400*cmdX/max_dist


        if cmdY <= 0:
            #send to y1 motor
            percent3 = 1500 - 400*cmdY/max_dist
            percent4 = 1500 - 400*cmdY/max_dist

        else:
            #send to y2 motor
            percent3 = 1500 + 400*cmdY/max_dist
            percent4 = 1500 + 400*cmdY/max_dist
            
        return [percent1, percent2, percent3, percent4]