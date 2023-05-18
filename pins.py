import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class signal_pin(object):
    def __init__(self, pin):
        self.pin = pin
        self.value = 0
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    
    def set(self, level):
        #level = 1 is HIGH; 0 is LOW
        if level == 1:
            GPIO.output(self.pin, GPIO.HIGH)
            print(self.pin, 'set to HIGH')
            self.value = 1
        else:
            GPIO.output(self.pin, GPIO.LOW)
            print(self.pin, 'set to LOW')
            self.value = 0
    
    def getvalue(self):
        return self.value
    
if __name__ == "__main__":
    s = signal_pin(17)
    s.set(1)