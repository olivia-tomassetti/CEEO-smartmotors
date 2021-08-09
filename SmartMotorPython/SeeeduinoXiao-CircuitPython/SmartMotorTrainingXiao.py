#SmartMotor Xiao CircuitPython Code 
    #This code trains the Smart Motor based on different sensor values. The user can train 
    #the motor to go to different positions/speeds based on differing light sensor values.
    #To switch from training to run mode, press and hold the single button, then press 
    #the same button again to retrain.

#Import necessary libraries
import time
import board
import pwmio
from adafruit_motor import servo
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction
import wifi

#Servo motor connected to A1
pwm1 = pwmio.PWMOut(board.A1, frequency=50)
my_servo = servo.Servo(pwm1)

#Initialize ports
Buzzer = DigitalInOut(board.D10)
LightSensor = AnalogIn(board.A8)
Potentiometer = AnalogIn(board.A2)
Button = DigitalInOut(board.D5)
LED = DigitalInOut(board.D9)
LED.direction=Direction.OUTPUT

def buzzer(repeats):
    for i in range(repeats):
        for i in range(4000):
            Buzzer.on()
            time.sleep(.0001)
            Buzzer.off()
            time.sleep(.0005)

        time.sleep(0.1)
        

def mapSensorRange(potValue):
    mappedValue = 26 + ((potValue)*(138-26))/943
    print(int(mappedValue))
    return int(mappedValue)

#Main loop
while True:
    print("in loop")
    training = [] #array to hold training values
    BuiltInLED.on() #turns built-in LED off
    LED.off()
    while True:
        while Button.value() == False:
            potValue = value.read()
            print(potValue)
            dutyValue = mapSensorRange(potValue)
            #Map potentiometer value to motor value
            my_servo.angle = dutyValue
            time.sleep(.01)
        print("Button pressed")
        angle = mapSensorRange(potValue)
        bright = value.read()
        pressTime = 0
        #Go to run mode if long press
        while  Button.value():
            BuiltInLED.off()
            LED.on()
            time.sleep(.1)
            pressTime += 0.1
            print(pressTime)
            if pressTime == 1.0:
                break
        BuiltInLED.on()
        LED.off()
        if pressTime > 1:
            break
        buzzer(1)
        #Add training to array
        training.append((angle,bright))
        print("Angle: " + str(angle))
        print("Brightness: " + str(bright))
    buzzer(2)
    BuiltInLED.off()
    LED.on()
    while  Button.value():
        time.sleep(.1)  

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
        my_servo.angle = pos
        time.sleep(.01)
        if Button.value() == True:
            break

    BuiltInLED.on()
    LED.off()
    buzzer(1)
    while  Button.value():
        time.sleep(.1)
