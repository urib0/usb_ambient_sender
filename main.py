import serial
import ambient
import time

TIME = 300

readSer = serial.Serial('hoge', 9600, timeout=3)

a = ambient.Ambient(33580, "hoge")

while 1:
    raw = readSer.readline().decode().replace('\n', '')
    line = raw.split(";")
    if line[0].split("=")[1].isdecimal():
        temp = int(line[0].split("=")[1]) / 100
        humid = int(line[1].split("=")[1]) / 100
        res = a.send({"d1": temp, "d2": humid}, timeout=60)
#        print( str(res) + "    " + str(temp) + "," + str(humid) )
    else:
        #        print(time.strftime("%Y/%m/%d/%H:%M:%S") + "," + str(raw))

    time.sleep(TIME)

readSer.close()
