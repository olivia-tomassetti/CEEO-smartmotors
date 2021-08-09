#Smart Motor Training Code for Rev1 Board
    #This code trains the Smart Motor based on different light sensor values. The user can train 
    #as many different positions and light sensor values as desired. To switch from training to 
    #run mode, press and hold the button, then press the same button again to retrain. 

#Import libraries
import machine
import time
from machine import Pin, ADC

#Initialize servo pin and set pwm frequency
p2 = machine.Pin(0)
pwm2 = machine.PWM(p2)
pwm2.freq(50)
pwm2.duty(90)

#Initialize digital pins
Buzzer = Pin(4, Pin.OUT)
BuiltInLED = Pin(2, Pin.OUT)
LightSensor = Pin(5, Pin.OUT)
Potentiometer = Pin(15, Pin.OUT)

Green = Pin(14, Pin.OUT)
Red = Pin(13, Pin.OUT)
Blue = Pin(12, Pin.OUT)
Button = Pin(16, Pin.IN)

#Turn LightSensor and Potentiometer digital pins LOW
LightSensor.value(0)
Potentiometer.value(0)

#Initialize analog pin
value = ADC(0)

#Play buzzer sound
def buzzer(repeats):
    for i in range(repeats):
        for i in range(4000):
            Buzzer.on()
            time.sleep(.0001)
            Buzzer.off()
            time.sleep(.0005)

        time.sleep(0.1)
        
#Map the potentiometer value to a valid motor position
def mapSensorRange(potValue):
    mappedValue = 26 + ((potValue)*(138-26))/943
    print(int(mappedValue))
    return int(mappedValue)

#Main loop
while True:
    LightSensor.value(0) 
    Potentiometer.value(0)
    print("in loop")
    training = [] #array to hold training values
    BuiltInLED.on() #turns built-in LED off
    Green.off()
    Blue.off()
    Red.off()
    while True:
        Potentiometer.value(0)
        LightSensor.value(0)
        Potentiometer.value(1) #turn on Potentiometer digital pin
        while Button.value() == False:
            potValue = value.read()
            print(potValue)
            #Map potentiometer value to motor value
            dutyValue = mapSensorRange(potValue)
            #Move motor to correct position
            pwm2.duty(dutyValue)
            time.sleep(.01)
        print("Button pressed")
        Potentiometer.value(0) #turn off Potentiometer digital pin
        LightSensor.value(1) #turn on LightSensor digital pin
        angle = mapSensorRange(potValue)
        bright = value.read()
        pressTime = 0
        #Go to run mode if long press
        while  Button.value():
            BuiltInLED.off()
            Blue.on()
            time.sleep(.1)
            pressTime += 0.1
            print(pressTime)
            if pressTime == 1.0:
                break
        BuiltInLED.on()
        Blue.off()
        if pressTime > 1:
            break
        buzzer(1)
        #Add training to array
        training.append((angle,bright))
        print("Angle: " + str(angle))
        print("Brightness: " + str(bright))

    #Buzz twice to indicate running mode
    buzzer(2)
    BuiltInLED.off()
    Green.on()
    while  Button.value():
        time.sleep(.1)  

    LightSensor.value(1) #turn on LightSensor digital pin

    #Run mode
    while True:
        print("In the loop")
        bright = value.read()
        print("Brightness: " + str(bright))
        min = 1000
        pos = 0
        for (a,l) in training:
            dist = abs(bright - l)
            if dist < min:
                min = dist
                pos = a
        #Move motor
        pwm2.duty(pos)
        time.sleep(.01)
        if Button.value() == True:
            break

    BuiltInLED.on()
    Green.off()
    buzzer(1)
    while  Button.value():
        time.sleep(.1)

