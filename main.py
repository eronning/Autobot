
# to figure out which tty port is being used run: dmesg | grep tty

import serial
import time
import findBeacon # return maximu value of lumi
import existObstacle # return bool value if obstacle is in front
import avoidObstacle # need to modify these function, if no obstacle around, should stop instead of moving fowrad

#while
 #step1 findBeacon(), if return value<threshhold_ambient go to step 3
 #step2 ifObstacle(), if yes go to step 3, if no go to step 4
 #step3 move forward one step, go back to step 1
 #step4 avoidObstacle(), go back to step 1
#rest at the beacon

threshhold_final = "?"     # reacod the max lum at 0 distance
threshhold_ambient = "?"   # record ambient value

ser = serial.Serial("/dev/ttyACM0", 115200)
ser_write = serial.Serial("/dev/ttyUSB0",9600)

ser.setDTR(True)
time.sleep(1)
er.setDTR(False)

def swrite(s)
 ser_write.write(s)
def sread()
 return int(ser.readline())

l

flag = 1;
while(sread< threshhold_final)
 if(flag==1)
  L_read = findbeacon()
  if(L_read <threshhold_ambinet)
    flag =3
  else 
   flag = 2
   while(sread()<L_read-20) # -20 tolerabce
    swrite("a");
   swrite("h")
   L_read = 0
 if(flag ==2)
   if(existObstacle)
    flag ==4
  flag ==3
 if(flag == 3)
  swrite("i")
  flag ==1
 if(flag == 4)
  avoidObstacle()
  flag==1

swrite("h")
