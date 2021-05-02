#!/usr/bin/env python3

import serial
import ambient
import time
import json
import datetime

f = open("./config.json", "r")
conf = json.loads(f.read())
f.close()


readSer = serial.Serial(conf["serial_port"], conf["serial_rate"], timeout=3)

a = ambient.Ambient(33580, conf["ambient_key_write"])

while 1:
    filename = datetime.datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    f = open(conf["logdir"] + "/" + filename + ".csv", mode="a")
    raw = readSer.readline().decode().replace('\n', '')
    line = raw.split(";")
    if line[0].split("=")[1].isdecimal():
        temp = int(line[0].split("=")[1]) / 100
        humid = int(line[1].split("=")[1]) / 100
        res = a.send({"d1": temp, "d2": humid}, timeout=60)
        row = str(timestamp) + "," + str(temp) + \
            "," + str(humid) + "," + str(raw)
    else:
        row = str(timestamp) + "," + "0.0,0.0," + "," + str(raw)
    f.write(row + "\n")
    f.close()
    time.sleep(conf["interval"])

readSer.close()
