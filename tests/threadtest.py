from threading import Thread
from time import sleep

x = 0

def getInput():
  global x
  while True:
    sleep(0.5)
    i = input("command: ")
    if i == "stop":
      end = True
      x = x+1
    

def sameTime():
  global x
  while True:
    print("TIMING", x)
    sleep(3)



t1 = Thread(target=getInput)
t2 = Thread(target=sameTime)

t1.start()
t2.start()

t1.join()
t2.join()

print("This always happens last")

