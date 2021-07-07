#Code to train Smart Motor with Buttons in place of potentiometer
import machine
import time
from machine import Pin, ADC

p2 = machine.Pin(0)
pwm2 = machine.PWM(p2)
pwm2.freq(50)

pwm2.duty(90)

#Initialize pins
LED = Pin(5, Pin.OUT)
BuiltInLED = Pin(2, Pin.OUT)
LightSensor = ADC(0)
Left = Pin(13, Pin.IN) 
Button = Pin(14, Pin.IN)
Right = Pin(15, Pin.IN)
print("about to enter")
while True:
    print("in loop")
    training = []
    #train for case A then B
    for case in range(2):
        LED.off()
        BuiltInLED.on()
        for counter in range(5):
            while Button.value() == False:
                time.sleep(.01)
                while(Left.value() == True and pwm2.duty() < 138):
                    print("Left")
                    dutyValue = pwm2.duty() + 1
                    print(dutyValue)
                    pwm2.duty(dutyValue)
                    LED.on()
                    BuiltInLED.off()
                    time.sleep(.05)
                    BuiltInLED.on()
                    LED.off()
                while(Right.value() == True and pwm2.duty() > 26):
                    print("Right")
                    dutyValue = pwm2.duty() - 1
                    pwm2.duty(dutyValue)
                    print(dutyValue)
                    LED.on()
                    BuiltInLED.off()
                    time.sleep(.05)
                    LED.off()
                    BuiltInLED.on()
            print("Button pressed")
            angle = pwm2.duty()
            bright = LightSensor.read()
            while  Button.value():
                LED.on()
                BuiltInLED.off()
                time.sleep(.1)
            LED.off()
            BuiltInLED.on()
            training.append((case,angle,bright))
            print(angle)
            print(bright)


    LED.on()
    BuiltInLED.off()
        
    # grab reading
    while True:
        print("In the loop")
        bright = LightSensor.read()
        min = 1000
        pos = 0
        for (c,a,l) in training:
            dist = abs(bright - l)
            if dist < min:
                min = dist
                pos = a
                val = c
        pwm2.duty(pos)
        time.sleep(.01)
        if Button.value() == True:
            break

    LED.off()
    BuiltInLED.on()