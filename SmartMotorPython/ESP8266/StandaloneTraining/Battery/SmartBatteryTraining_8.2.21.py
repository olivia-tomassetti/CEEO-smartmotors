#Smart Battery Training
    #This codes allows the user to train either a speaker or a motor depending
    #on the actuator mode. The mode can be switched by pressing the button two
    #times fast. To switch from training to run mode, press and hold the button, 
    #then press the same button again to retrain. 

#Import libraries
import machine
import time
from machine import Pin, ADC

#Initialize pwm pin and set pwm frequency
D3 = machine.Pin(0)
pwm0 = machine.PWM(D3)
pwm0.freq(50)
pwm0.duty(90)


#Initialize digital pins
Buzzer = Pin(4, Pin.OUT)
BuiltInLED = Pin(2, Pin.OUT)
LightSensor = Pin(5, Pin.OUT)
Potentiometer = Pin(15, Pin.OUT)
Button = Pin(16, Pin.IN)
Blue = Pin(13, Pin.OUT)
Green = Pin(12, Pin.OUT)

#Turn LightSensor, Potentiometer, and LED digital pins LOW
LightSensor.value(0)
Potentiometer.value(0)
Blue.off()
Green.off()

#Initialize analog pin
value = ADC(0)

#Play buzzer sound
def buzzer(repeats):
    for i in range(repeats):
        for i in range(1000):
            Buzzer.on()
            time.sleep(.0001)
            Buzzer.off()
            time.sleep(.0005)

        time.sleep(0.01)
        
#Map the potentiometer value to a valid motor position 
def mapDutySensorRange(potValue):
    mappedDutyValue = 26 + ((potValue)*(138-26))/943
    return int(mappedDutyValue)

#Map the potentiometer value to a valid note frequency 
def mapFreqSensorRange(potValue):
    if potValue <10:
        mappedValue = 0
        #pwm12.duty(0)
        #pwm12.freq(0)
    elif potValue < 110:
        mappedValue = 262
        #pwm12.duty(90)
    elif potValue < 220:
        mappedValue = 294
        #pwm12.duty(90)
    elif potValue < 330:
        mappedValue = 330
        #pwm12.duty(90)
    elif potValue < 440:
        mappedValue = 349
        #pwm12.duty(90)
    elif potValue < 550:
        mappedValue = 392
        #pwm12.duty(90)
    elif potValue < 660:
        mappedValue = 440
        #pwm12.duty(90)
    elif potValue < 770:
        mappedValue = 494
        #pwm12.duty(90)
    else:
        mappedValue = 523

    return int(mappedValue)

#Check whether the button is pressed long enough to be put into run mode
#or whether the button is pressed two times fast to change actuator mode
def pressedButton(mode):
    global oldPressTime
    buttonPressTime = time.time_ns()
    print("Old press: " + str(oldPressTime))
    print("Button press: " + str(buttonPressTime))
    print("Diff press: " + str(buttonPressTime-oldPressTime))
    pressTime = 0
    while  Button.value():
        if mode == 1:
            Green.on()
        elif mode == 2:
            Blue.on()
        BuiltInLED.off()
    Green.off()
    Blue.off()
    if time.time_ns()-buttonPressTime > 1000000000:
        mode = 3 #run mode
    elif buttonPressTime - oldPressTime < 400000000: #switch actuator mode
        print("switch")
        print("Old press: " + str(oldPressTime - buttonPressTime))
        print("Button press: " + str(buttonPressTime))
        if mode == 1:
            mode = 2 
        elif mode == 2:
            pwm0.freq(50)
            mode = 1
        print("Mode "+str(mode))
    else:
        mode = mode
    oldPressTime = time.time_ns()
    return mode

actuatorMode = 1 #start with motor mode
oldPressTime = 0

#Main loop
while True:
    LightSensor.value(0)
    Potentiometer.value(0)
    print("in loop")
    trainingMotor = [] #array to hold motor training values
    trainingSpeaker = [] #array to hold speaker training values
    BuiltInLED.on() #turns built-in LED off
    LED.off()
    while True:
        Potentiometer.value(0)
        LightSensor.value(0)
        while Button.value() == False:
            Potentiometer.value(1)
            potValue = value.read()
            if actuatorMode == 1:
                dutyValue = mapDutySensorRange(potValue)
                pwm0.duty(dutyValue)
            elif actuatorMode == 2:
                freqValue = mapFreqSensorRange(potValue)
                pwm0.freq(freqValue)
            time.sleep(.01)
        print("Button pressed")

        #Switch which sensor is being read
        Potentiometer.value(0)
        LightSensor.value(1)
        
        #Read sensor value
        bright = value.read()
        time.sleep(0.1)

        #Check button "pattern" for mode
        mode = pressedButton(actuatorMode)

        #Map pot value
        dutyValue = mapDutySensorRange(potValue)
        freqValue = mapFreqSensorRange(potValue)

        BuiltInLED.on()

        if mode == 1:
            actuatorMode = 1
            trainingMotor.append((dutyValue,bright))
            print("Angle: " + str(dutyValue))
        elif mode == 2:
            actuatorMode = 2
            trainingSpeaker.append((freqValue,bright))
            print("Note: " + str(freqValue))
        elif mode == 3:
            print("break")
            break

        buzzer(1)
        print("Brightness: " + str(bright))

    #Buzz twice indicating run mode
    buzzer(2)
    BuiltInLED.off()
    while  Button.value():
        time.sleep(.1)  

    LightSensor.value(1)
    
    if actuatorMode == 1:
        Green.on()
        training = trainingMotor
    elif actuatorMode == 2:
        Blue.on()
        training = trainingSpeaker

    #Run mode
    while True:
        print("In the loop")
        bright = value.read()
        print("Brightness: " + str(bright))
        min = 1000
        pos = 0
        sound = 0
        for (a,l) in training:
            dist = abs(bright - l)
            if dist < min:
                min = dist
                pos = a
        if actuatorMode == 1:
            pwm0.duty(pos)
        elif actuatorMode == 2:
            pwm0.freq(pos)
        time.sleep(.01)
        if Button.value() == True:
            break

    BuiltInLED.on()
    Blue.off()
    Green.off()
    
    buzzer(1)
    while  Button.value():
        time.sleep(.1)





