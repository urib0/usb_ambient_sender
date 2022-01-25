#!/usr/bin/env python3
# python3.7で動作確認済み

import serial
import ambient
import time
import json
import datetime as dt
import sys
import random
import os
import subprocess
import requests

DEBUG = False
REPETITIONS = 3

def conv(data):
    if data.split("=")[0] in {"temp", "hum"}:
        return int(data.split("=")[1]) / 100
    else:
        return int(data.split("=")[1])


# 設定値読み込み
f = open("/home/pi/work/usb_ambient_sender/config.json", "r")
conf = json.loads(f.read())
f.close()

am = ambient.Ambient(conf["ambient_channel"], conf["ambient_key_write"])

data_dic = {}
for device in conf["devices"]:
    data_arr = []
    if "cpu_temp" == device["sensor_name"]:
        cmd = 'cat /sys/class/thermal/thermal_zone0/temp'
        data = int((subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                        shell=True).communicate()[0]).decode('utf-8').split("\n")[0])/1000.0
        data_arr.append(str(data))
        data_dic[device["sensors"][0]] = data
    else:
        filename = conf["logdir"] + "/" + device["sensor_name"] + "/" + device["sensor_name"] + "_" + dt.datetime.now().strftime("%Y-%m-%d") + ".csv"
        print(filename)
        try:
            f = open(filename,"r")
            lines = f.readlines()[-1:][0][:-1]
            f.close
            print(lines)
        except Exception as e:
            pass
        


        
        # シリアル読み込み
        readSer = serial.Serial(
            device["serial_port"], device["serial_rate"], timeout=3)
        raw = readSer.readline().decode().replace('\n', '')
        readSer.close()

        print(int(raw.split(";")[0].split("=")[1]))
        # データ整形
        for j in range(len(device["sensors"])):
            d = conv(raw.split(";")[j])
            data_dic[device["sensors"][j]] = d
            data_arr.append(str(d))
        data_arr.append(raw)

# ambient送信処理
for i in range(REPETITIONS):
    try:
        res = am.send(data_dic, timeout=10)
        print('sent to Ambient (ret = %d)' % res.status_code)
        if res.status_code == 200:
            break
    except requests.exceptions.RequestException as e:
        print('request failed: ', e)
