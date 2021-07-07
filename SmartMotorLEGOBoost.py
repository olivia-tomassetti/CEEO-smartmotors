from pybricks.hubs import CityHub
from pybricks.pupdevices import Motor, ColorDistanceSensor
from pybricks.parameters import Port, Stop, Color
from pybricks.tools import wait

# Initialize devices.
hub = CityHub()
motor = Motor(Port.B)
colorSensor = ColorDistanceSensor(Port.A)

while True:  
    colors = []
    angles = [] 
    #Mode 1 - Train
    hub.light.on(Color.WHITE)
    wait(500)
    hub.light.off()
    wait(500)
    hub.light.on(Color.WHITE)
    wait(500)
    hub.light.off()
    wait(500)
    hub.light.on(Color.WHITE)
    wait(500)
    #Train for 4 color cases
    for case in range(4):
        #5 trainings for each case
        for i in range(5):
            try:
                while True:
                    color = colorSensor.color() 
                    hub.light.on(color)
                    wait(100)
            except SystemExit:
                pass
            #Get color
            color = colorSensor.color() 
            print(color)
            #Turn hub light color of sensor reading
            hub.light.on(color)
            #Get motor angle
            angle = motor.angle()
            print(angle)
            #Add the sensor reading and motor angle to list
            colors.append(color)
            angles.append(angle)
            wait(100)
        hub.light.on(Color.WHITE)
        wait(2000)
    
    print(colors)
    print(angles)
    
    #Mode 2 - Run
    try: 
        while True:
            counter = 0
            avgPos = 0
            sumPos = 0
            #Get color sensor reading
            color = colorSensor.color()
            hub.light.on(color)
            if color != Color.NONE:
                for i in range(len(colors)):
                    #Find average position reading for sensed color
                    if colors[i] == color:
                        counter = counter + 1 
                        sumPos = (sumPos+angles[i])
                avgPos = sumPos/counter
                print(avgPos)
                #Move motor to average position at 400 (can change speed)
                motor.run_target(400, avgPos)
                motor.stop()
            wait(500)
            
    except SystemExit:
        try: 
            wait(1000)
            break
        except SystemExit:
            pass
