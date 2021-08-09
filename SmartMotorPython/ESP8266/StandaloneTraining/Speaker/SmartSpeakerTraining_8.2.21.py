#Smart Speaker Training Code
    #This code currently adjusts the pwm frequency based on the sensor value.
    #Therefore, it is able to train a speaker vs a motor. The code can be 
    #modified to train a motor by replacing pwm2.freq() with pwm2.duty() and 
    #the call for mapFreqSensorRange(potValue) with mapDutySensorRange(potValue)

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
def mapDutySensorRange(potValue):
    mappedValue = 20 + ((potValue)*(130-20))/943
    return int(mappedDutyValue)

#Map the potentiometer value to a valid note frequency 
def mapFreqSensorRange(potValue):
    if potValue <10:
        mappedValue = 0
        pwm2.duty(0)
    elif potValue < 110:
        mappedValue = 262
        #pwm2.duty(90)
    elif potValue < 220:
        mappedValue = 294
        #pwm2.duty(90)
    elif potValue < 330:
        mappedValue = 330
        #pwm2.duty(90)
    elif potValue < 440:
        mappedValue = 349
       # pwm2.duty(90)
    elif potValue < 550:
        mappedValue = 392
       # pwm2.duty(90)
    elif potValue < 660:
        mappedValue = 440
        #pwm2.duty(90)
    elif potValue < 770:
        mappedValue = 494

    else:
        mappedValue = 523

    return int(mappedFreqValue)

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
        while Button.value() == False:
            Potentiometer.value(1)
            potValue = value.read()
            dutyValue = mapFreqSensorRange(potValue) #map potentiometer value to speaker frequency value
            pwm2.freq(dutyValue) #change frequency for speaker
            time.sleep(.01)
        print("Button pressed")
        Potentiometer.value(0)
        LightSensor.value(1)
        note = pwm2.freq()
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
        print("Note: " + str(note))
        print("Brightness: " + str(bright))
    buzzer(2)
    BuiltInLED.off()
    Green.on()
    while  Button.value():
        time.sleep(.1)  

    #Turn LightSensor pin HIGH
    LightSensor.value(1)

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
        pwm2.freq(pos)
        if pos == 0:
            pwm2.duty(0)
        else:
            pwm2.duty(90)
        time.sleep(.01)
        
        if Button.value() == True:
            break

    BuiltInLED.on()
    Green.off()
    buzzer(1)
    while  Button.value():
        time.sleep(.1)





