


referenceX = 0
referenceY = 0

def set_zero(zeroX, zeroY):
    referenceX = zeroX
    referenceY = zeroY

def PID(x, y):
    referenceX = 0
    referenceY = 0

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

    currentX = x
    currentY = y
    # Implement moving average
    errorX = referenceX - currentX
    errorY = referenceY - currentY

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
    percent3 = 0 # x3
    percent4 = 0 # x4
    # Hypothetical Max = .5m
    # Velocity = distance/time

    if cmdX <= 0:
        #send to x1 motor
        percent1 = -cmdX/max_dist
        percent2 = -cmdX/max_dist

    if cmdX > 0:
        #send to x2 motor
        percent2 = cmdX/max_dist
        percent1 = cmdX/max_dist


    if cmdY <= 0:
        #send to y1 motor
        percent3 = -cmdY_max_dist
        percent4 = -cmdY/max_dist

    if cmdY > 0:
        #send to y2 motor
        pass
        percent3 = cmdY/max_dist
        percent4 = cmdY/max_dist

        
    return [percent1, percent2, percent3, percent4]
