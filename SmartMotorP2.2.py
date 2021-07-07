import machine
import time
from machine import Pin, ADC

p2 = machine.Pin(0)
pwm2 = machine.PWM(p2)

pwm2.duty(90)

#Initialize pins
LED = Pin(5, Pin.OUT)
LightSensor = ADC(0)
#Buzzer = Pin(14, Pin.OUT)
Left = Pin(13, Pin.IN) 
Button = Pin(12, Pin.IN)
Right = Pin(14, Pin.IN)

#t = [ [0]*5 for i in range(2)]

run = 0
count = 0

while True: 
    LED.off()
    if run == 0:
        while(Left.value() == True and pwm2.duty() < 138):
            print("Left")
            dutyValue = pwm2.duty() + 1
            print(dutyValue)
            pwm2.duty(dutyValue)
            LED.on()
            time.sleep(.05)
            
        while(Right.value() == True and pwm2.duty() > 26):
            print("Right")
            dutyValue = pwm2.duty() - 1
            pwm2.duty(dutyValue)
            print(dutyValue)
            LED.on()
            time.sleep(.05)
        
        if(Button.value()==True):
            print("Button")
            while(Button.value() == True):
                time.sleep(.05)
            dutyValue = pwm2.duty()
            print(dutyValue)
            lightValue = LightSensor.read()
            print(lightValue)
            if(count<0):
                count = 0
            elif(count>=0 and count<5):
                training.append(dutyValue,lightValue)
            else:
                run = 1
                while(Button.value() == False):
                    LED.on()
                    brightness = LightSensor.read()
                    minimum = 1000
                    pos = 0
                    for (c,a,l) in training:
                        dist = abs(brightness - training[i])
                        if(dist<minimum):
                            minimum = dist
                            dutyValue = training[i]
                    pwm2.duty(dutyValue)
                    time.sleep(0.1)

                count = 0
                LED.off()

            time.sleep(0.05)

#Training loop
while True:
    LED.off()
    while not Button.value:
        time.sleep(.01)
    angle = pwm2.duty()
    bright = LightSensor.read()
    buttonPress = 0
    while  Button.value:
        buttonPress += 1
        if buttonPress == 20:
            break
        time.sleep(.1)
    if buttonPress == 20:
        break
    training.append((angle,bright))

LED.off()
print("training")
