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

#Code to test servo motor range
i = 26
for i in range(26,140): #input range
    pwm2.duty(i)
    print(i)
    time.sleep(0.1)

#Code for testing potentiometer readings
Potentiometer.value(1)
LightSensor.value(0)
while True:
    potValue = value.read()
    print(potValue)
    time.sleep(0.1)