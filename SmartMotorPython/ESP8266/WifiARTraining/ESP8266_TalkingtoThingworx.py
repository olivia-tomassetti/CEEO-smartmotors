import network,usocket,ussl,utime,ujson,ubinascii
import machine
from machine import Pin, ADC

p2 = machine.Pin(0)
pwm2 = machine.PWM(p2)

def wifi():
    wlan = network.WLAN()
    wlan.active(True)
    wlan.connect("Tufts_Wireless", "")
    mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
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
LightSensor = ADC(0)
i = 0
while True:
    i += 1
    for case in range(2):
        if case == 0:
            PORT = 443
            base='pp-21060114127e.portal.ptc.io'
            request='GET /Thingworx/Things/ESP8266_SmartMotor/Properties/MotorPosition HTTP/1.1\r\n'
            request += 'Host: pp-21060114127e.portal.ptc.io\r\n'
            request += 'Content-Type: application/json\r\n'
            request += 'Accept: application/json\r\n'
            request += 'appKey: 9ea85a72-9535-4531-9d91-e4ff86dab458\r\n\r\n'
        elif case == 1:
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
        elif case == 2:
            PORT = 443
            payload2 = {"MotorPosition": pwm2.duty()}
            payload2 = ujson.dumps(payload2)
            base='pp-21060114127e.portal.ptc.io'
            request='PUT /Thingworx/Things/ESP8266_SmartMotor/Properties/MotorPosition HTTP/1.1\r\n'
            request += 'Host: pp-21060114127e.portal.ptc.io\r\n'
            request += 'Content-Type: application/json\r\n'
            request += 'Accept: application/json\r\n'
            request += 'appKey: 9ea85a72-9535-4531-9d91-e4ff86dab458\r\n'
            request += 'Content-Length: %d\r\n\r\n' % len(payload2)
            request += '%s\r\n\r\n' % payload2
    
                
        if False : print(case,request.encode())
        status, reason, reply = test(base, PORT, request, True)
        
        if status < 0:
            print(status,reason,reply)
            continue
        if case == 0:
            reply =  ujson.loads(reply.split('\r\n')[1])['rows'][0]
        elif case == 1:
            reply =  reply
        elif case == 2:
            reply = reply
        print(status, reason, reply)
        print()
    utime.sleep(2)
