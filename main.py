import serial
import ambient
import time
import json

TIME = 300

f = open("./config.json", "r")
conf = json.loads(f.read())
f.close()


readSer = serial.Serial(conf["serial_port"], conf["serial_rate"], timeout=3)

a = ambient.Ambient(33580, conf["ambient_key_write"])

while 1:
    raw = readSer.readline().decode().replace('\n', '')
    line = raw.split(";")
    if line[0].split("=")[1].isdecimal():
        temp = int(line[0].split("=")[1]) / 100
        humid = int(line[1].split("=")[1]) / 100
        res = a.send({"d1": temp, "d2": humid}, timeout=60)
#        print( str(res) + "    " + str(temp) + "," + str(humid) )
#    else:
#        print(time.strftime("%Y/%m/%d/%H:%M:%S") + "," + str(raw))
    time.sleep(TIME)

readSer.close()
