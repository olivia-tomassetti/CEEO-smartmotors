'''SmartBattery Xiao CircuitPython Code
    **the final version of this code is still in progress** 

    This code trains the Smart Actuator (can plug in a motor or speaker) based on different 
    sensor values. The user can train the motor or speaker to go to different positions/speeds 
    or different notes respectively based on varying sensor readings.To switch from training to 
    run mode, press and hold the single button, then press the same button again to retrain. 
    To switch from motor to speaker mode or visa versa press the button two times fast in a row.
    '''

import time
import board
import pwmio
from adafruit_motor import servo
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
import wifi

#Servo motor or speaker connected to A1
pwm1 = pwmio.PWMOut(board.A1, frequency=50, variable_frequency=True)
my_servo = servo.Servo(pwm1)

#Speaker connected to A2 - this is another way to try it
#pwm2 = pwmio.PWMOut(board.A2, frequency=50, variable_frequency=True)

#Initialize Analog pins
LightSensor = AnalogIn(board.A8)
Potentiometer = AnalogIn(board.A9)

#Initialize digital pins
Buzzer = DigitalInOut(board.D10)
Buzzer.direction = Direction.OUTPUT
GLED = DigitalInOut(board.D4)
GLED.direction=Direction.OUTPUT
BLED = DigitalInOut(board.D3)
BLED.direction=Direction.OUTPUT
Button = DigitalInOut(board.D5)
Button.direction = Direction.INPUT
Button.pull = Pull.DOWN

#Play buzzer sound
def buzzer(repeats):
    for i in range(repeats):
        for i in range(700):
            Buzzer.value = True
            time.sleep(.0001)
            Buzzer.value = False
            time.sleep(.0005)

        time.sleep(0.05)
        
#Map the potentiometer value to a valid motor position
def mapDutySensorRange(potValue):
    mappedMotorValue = ((potValue-256)*(180))/(65520-256)
    return int(mappedMotorValue)

#Map the lightsensor value to 10-1024
def mapLightRange(LightSensor):
    mappedLightValue = ((LightSensor-1000)*(1024))/40000
    return int(mappedLightValue)

#Map the potentiometer value to a valid note frequency
def mapFreqSensorRange(potValue):
    if potValue < 6000
        mappedValue = 1
    elif potValue < 8190:
        mappedValue = 262
    elif potValue < 16380:
        mappedValue = 294
    elif potValue < 24570:
        mappedValue = 330
    elif potValue < 32760:
        mappedValue = 349
    elif potValue < 40950:
        mappedValue = 392
    elif potValue < 49140:
        mappedValue = 440
    elif potValue < 57330:
        mappedValue = 494
    else:
        mappedValue = 523
    return int(mappedValue)

#Check whether the button is pressed long enough to be put into run mode
#or whether the button is pressed fast twice in a row to change actuator mode
def pressedButton(mode):
    global oldPressTime
    buttonPressTime = time.monotonic()
    print("Old press: " + str(oldPressTime))
    print("Button press: " + str(buttonPressTime))
    print("Diff press: " + str(buttonPressTime-oldPressTime))
    pressTime = 0
    while  Button.value:
        #Green if in motor mode
        if mode == 1:
            GLED.value = True 
        #Blue if in speaker mode
        elif mode == 2:
            BLED.value = True
    GLED.value = False
    BLED.value = False
    if time.monotonic() - buttonPressTime > 1.5:
        mode = 3 #signifies run mode
    #If pressed fast --> switch actuator mode
    elif buttonPressTime - oldPressTime < 0.9: 
        print("switch")
        if mode == 1:
            mode = 2
            pwm1.duty_cycle = 0
        elif mode == 2:
            pwm1.frequency = 50
            mode = 1
        print("Mode "+str(mode))
    else:
        mode = mode
    oldPressTime = time.monotonic()
    return mode

actuatorMode = 1 #start with motor mode
oldPressTime = 0

#Main loop
while True:
    print("in loop")
    trainingMotor = [] #array to hold motor training values
    trainingSpeaker = [] #array to hold speaker training values
    GLED.value = False
    BLED.value = False
    while True:
        while Button.value == False:
            potValue = Potentiometer.value #get potentiometer value
            if actuatorMode == 1:
                dutyValue = mapDutySensorRange(potValue)
                my_servo.angle = dutyValue
            elif actuatorMode == 2:
                freqValue = mapFreqSensorRange(potValue)
                pwm1.frequency = freqValue
            potValue = Potentiometer.value
            time.sleep(.01)
        print("Button pressed")
        bright = mapLightRange(LightSensor.value)
        #Check button "pattern" for mode
        mode = pressedButton(actuatorMode)
        dutyValue = mapDutySensorRange(potValue)
        freqValue = mapFreqSensorRange(potValue)
        #Append training to proper array based on actuator mode
        if mode == 1:
            actuatorMode = 1
            trainingMotor.append((dutyValue,bright))
            print("Angle: " + str(dutyValue))
        elif mode == 2:
            actuatorMode = 2
            trainingSpeaker.append((freqValue,bright))
            print("Note: " + str(freqValue))
        #Go to run mode if long press
        elif mode == 3:
            print("break")
            break
        buzzer(1)
        print("Brightness: " + str(bright))

    #Buzz twice to signify run mode
    buzzer(2)

    while  Button.value:
        time.sleep(.1)

    #LED constant color depending on actuator mode  
    if actuatorMode == 1:
        GLED.value = True
        training = trainingMotor
    elif actuatorMode == 2:
        BLED.value = True
        training = trainingSpeaker

    #Run mode
    while True:
        print("In the loop")
        bright = mapLightRange(LightSensor.value)
        print("Brightness: " + str(bright))
        min = 1000
        pos = 0
        for (a,l) in training:
            dist = abs(bright - l)
            if dist < min:
                min = dist
                pos = a
        if actuatorMode == 1:
            my_servo.angle = pos
        elif actuatorMode == 2:
            pwm1.frequency = pos
        time.sleep(.01)
        
        time.sleep(.01)
        if Button.value == True:
            break

    GLED.value = False
    BLED.value = False
    
    #Buzz once to signify return to training mode
    buzzer(1)
    while  Button.value:
        time.sleep(.1)
