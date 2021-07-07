#Code to train Smart Motor with Buttons in place of potentiometer
import network,usocket,ussl,utime,ujson,ubinascii
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


def wifi():
    wlan = network.WLAN()
    wlan.active(True)
    wlan.connect("Tufts_Wireless", "")
    mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
    print("Connected")
    return wlan.ifconfig()

def test(base, port, request, verbose = False ):
    addr = usocket.getaddrinfo(base, port)[0][4]
    if verbose: print(addr)
    client = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
    client.connect(addr)
    client.settimeout(3.0)
    if PORT == 443:
        try:
            client = ussl.wrap_socket(client, server_hostname=base)
        except Exception as e:
            if verbose:
                print('problem with ussl')
                print(e)
            return -1,'',''
    client.write(request)

    l = client.readline()
    if verbose: print(l)
    l = l.split(None, 2)
    status = int(l[1])
    reason = ''
    if len(l) > 2:
        reason = l[2].rstrip()
    if not (status == 200): return status, reason, ''
    l = client.readline()
    reply_h ={}
    if verbose: print(b' -' +l)
    while l and not l == b'\r\n':
        l = l.decode()
        k, v = l.split(":", 1)
        reply_h[k.lower()] = v.strip()
        l = client.readline()
        if verbose: print(b' --' + l)
    try:
        length = int(reply_h['content-length'])
        reply=client.read(length).decode()
        if verbose: print('LENGTH')
        if verbose: print(reply)
    except:
        if verbose: print('CHUNK')
        reply =''
        l = client.readline()
        while l and not l == b'\r\n':
            if verbose: print(b' ---  ' + l)
            reply += l.decode()
            l = client.readline()

        if verbose: print(reply)
    return status, reason, reply

while True:
    training = []
    SaveTraining = 0
    #train for case A then B
    for case in range(2):
        BuiltInLED.on()
        LED.off()
        for counter in range(5):
            while SaveTraining == 0:
                for message in range(2):
                    if message == 0:
                        print("Getting Motor reading")
                        PORT = 443
                        base='pp-21060114127e.portal.ptc.io'
                        request='GET /Thingworx/Things/ESP8266_SmartMotor/Properties/MotorPosition HTTP/1.1\r\n'
                        request += 'Host: pp-21060114127e.portal.ptc.io\r\n'
                        request += 'Content-Type: application/json\r\n'
                        request += 'Accept: application/json\r\n'
                        request += 'appKey: 9ea85a72-9535-4531-9d91-e4ff86dab458\r\n\r\n'
                        print("Motor Readinggggg")
                    elif message == 1:
                        print("Train?")
                        PORT = 443
                        base='pp-21060114127e.portal.ptc.io'
                        request='GET /Thingworx/Things/ESP8266_SmartMotor/Properties/SaveTraining HTTP/1.1\r\n'
                        request += 'Host: pp-21060114127e.portal.ptc.io\r\n'
                        request += 'Content-Type: application/json\r\n'
                        request += 'Accept: application/json\r\n'
                        request += 'appKey: 9ea85a72-9535-4531-9d91-e4ff86dab458\r\n\r\n'
                        print("Training decision recieved")

                    if False : print(message,request.encode())
                    status, reason, reply = test(base, PORT, request, True)

                    if status < 0:
                        print(status,reason,reply)
                        continue
                    if message == 0:
                        reply =  ujson.loads(reply.split('\r\n')[1])['rows'][0]
                        angle = int(reply['MotorPosition'])
                        pwm2.duty(angle)
                    if message == 1:
                        reply =  ujson.loads(reply.split('\r\n')[1])['rows'][0]
                        SaveTraining = int(reply['SaveTraining'])
                    print(status, reason, reply)
                    print()
        

            print("Button pressed")
            bright = LightSensor.read()
            training.append((case,angle,bright))
            print(angle)
            print(bright)

            PORT = 443
            payload = {"SaveTraining": 0}
            payload = ujson.dumps(payload)
            base='pp-21060114127e.portal.ptc.io'
            request='PUT /Thingworx/Things/ESP8266_SmartMotor/Properties/SaveTraining HTTP/1.1\r\n'
            request += 'Host: pp-21060114127e.portal.ptc.io\r\n'
            request += 'Content-Type: application/json\r\n'
            request += 'Accept: application/json\r\n'
            request += 'appKey: 9ea85a72-9535-4531-9d91-e4ff86dab458\r\n'
            request += 'Content-Length: %d\r\n\r\n' % len(payload)
            request += '%s\r\n\r\n' % payload
            if False : print(case,request.encode())
            status, reason, reply = test(base, PORT, request, True)
            reply = reply

            
    LED.on()
    BuiltInLED.off()
        
        # grab reading
    while True:
        print("In the loop")
        bright = LightSensor.read()
        PORT = 443
        payload = {"LightSensor": LightSensor.read()}
        payload = ujson.dumps(payload)
        base='pp-21060114127e.portal.ptc.io'
        request='PUT /Thingworx/Things/ESP8266_SmartMotor/Properties/LightSensor HTTP/1.1\r\n'
        request += 'Host: pp-21060114127e.portal.ptc.io\r\n'
        request += 'Content-Type: application/json\r\n'
        request += 'Accept: application/json\r\n'
        request += 'appKey: 9ea85a72-9535-4531-9d91-e4ff86dab458\r\n'
        request += 'Content-Length: %d\r\n\r\n' % len(payload)
        request += '%s\r\n\r\n' % payload
        if False : print(case,request.encode())
        status, reason, reply = test(base, PORT, request, True)
        reply = reply

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
        if SaveTraining == 1:
            break

    LED.off()
    BuiltInLED.on()





#--------------------------------------------------------------------------------

BuiltInLED
        
                


# grab reading
while True:
    bright = LightSensor.read()
    min = 1000
    pos = 0
    for (a,l) in training:
        dist = abs(bright - l)
        if dist < min:
            min = dist
            pos = a
    pwm2.duty(pos)
    time.sleep(.01)







training = []
#train for case A then B
for case in range(2):
    LED.off()
    for counter in range(5):
        while Button.value() == False:
            time.sleep(.01)
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
        print("Button pressed")
        bright = LightSensor.read()
        for message in range(2):
            print("message: " + str(message))
            print("in loop")
            if message == 0:
                PORT = 443
                payload = {"LightSensor": bright}
                payload = ujson.dumps(payload)
                base='pp-21060114127e.portal.ptc.io'
                request='PUT /Thingworx/Things/ESP8266_SmartMotor/Properties/LightSensor HTTP/1.1\r\n'
                request += 'Host: pp-21060114127e.portal.ptc.io\r\n'
                request += 'Content-Type: application/json\r\n'
                request += 'Accept: application/json\r\n'
                request += 'appKey: 9ea85a72-9535-4531-9d91-e4ff86dab458\r\n'
                request += 'Content-Length: %d\r\n\r\n' % len(payload)
                request += '%s\r\n\r\n' % payload
                print("send light")
            elif message == 1:
                print("Getting Motor reading")
                PORT = 443
                base='pp-21060114127e.portal.ptc.io'
                request='GET /Thingworx/Things/ESP8266_SmartMotor/Properties/MotorPosition HTTP/1.1\r\n'
                request += 'Host: pp-21060114127e.portal.ptc.io\r\n'
                request += 'Content-Type: application/json\r\n'
                request += 'Accept: application/json\r\n'
                request += 'appKey: 9ea85a72-9535-4531-9d91-e4ff86dab458\r\n\r\n'
                print("Motor Readinggggg")

            if False : print(message,request.encode())
            status, reason, reply = test(base, PORT, request, True)
    
            if status < 0:
                print(status,reason,reply)
                continue
            if message == 0:
                reply = reply
            if message == 1:
                reply =  ujson.loads(reply.split('\r\n')[1])['rows'][0]
                angle = int(reply['MotorPosition'])
                pwm2.duty(angle)
            print(status, reason, reply)
            print()

        while  Button.value():
            time.sleep(.1)
        
        training.append((case,angle,bright))
        print(angle)
        print(bright)


LED.on()
    
# grab reading
while True:
    bright = LightSensor.read()
    min = 1000
    pos = 0
    for (a,l) in training:
        dist = abs(bright - l)
        if dist < min:
            min = dist
            pos = a
            val = c
    pwm2.duty(pos)
    time.sleep(.01)







PORT = 443
                payload = {"LightSensor": bright}
                payload = ujson.dumps(payload)
                base='pp-21060114127e.portal.ptc.io'
                request='PUT /Thingworx/Things/ESP8266_SmartMotor/Properties/LightSensor HTTP/1.1\r\n'
                request += 'Host: pp-21060114127e.portal.ptc.io\r\n'
                request += 'Content-Type: application/json\r\n'
                request += 'Accept: application/json\r\n'
                request += 'appKey: 9ea85a72-9535-4531-9d91-e4ff86dab458\r\n'
                request += 'Content-Length: %d\r\n\r\n' % len(payload)
                request += '%s\r\n\r\n' % payload

      PORT = 443
                payload2 = {"MotorPosition": angle}
                payload2 = ujson.dumps(payload2)
                base='pp-21060114127e.portal.ptc.io'
                request='PUT /Thingworx/Things/ESP8266_SmartMotor/Properties/MotorPosition HTTP/1.1\r\n'
                request += 'Host: pp-21060114127e.portal.ptc.io\r\n'
                request += 'Content-Type: application/json\r\n'
                request += 'Accept: application/json\r\n'
                request += 'appKey: 9ea85a72-9535-4531-9d91-e4ff86dab458\r\n'
                request += 'Content-Length: %d\r\n\r\n' % len(payload2)
                request += '%s\r\n\r\n' % payload2
                print("Send motor")