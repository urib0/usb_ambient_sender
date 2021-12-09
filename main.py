#!/usr/bin/env python3
# python3.7で動作確認済み

import serial
import ambient
import time
import json
import datetime
import random
import os
import subprocess
import requests

DEBUG = False
REPETITIONS = 3
THRESHOLD = 2000

def logging(name, data):
    filename = name + "_" + datetime.datetime.now().strftime("%Y-%m-%d") + ".csv"
    timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    write_str = timestamp + "," + data
    path = "/home/pi/work/usb_ambient_sender/" + conf["logdir"] + "/" + name + "/"

    if DEBUG:
        print(write_str)

    os.makedirs(path, exist_ok=True)
    f = open(path + filename, mode="a")
    f.write(write_str + "\n")
    f.close()


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
for i in conf["devices"]:
    data_arr = []
    if "cpu_temp" == i["sensor_name"]:
        cmd = 'cat /sys/class/thermal/thermal_zone0/temp'
        data = int((subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                        shell=True).communicate()[0]).decode('utf-8').split("\n")[0])/1000.0
        data_arr.append(str(data))
        data_dic[i["sensors"][0]] = data
    else:
        # シリアル読み込み
        readSer = serial.Serial(
            i["serial_port"], i["serial_rate"], timeout=3)
        raw = readSer.readline().decode().replace('\n', '')
        readSer.close()

        print(int(raw.split(";")[0].split("=")[1]))
        if i["sensor_name"] == "th" and (int(raw.split(";")[0].split("=")[1]) > THRESHOLD ):
            url99 = "https://notify-api.line.me/api/notify"
            token = 'hoge'
            message  = '部屋の情報\n'
            message += '温度:'+str(int(raw.split(";")[0].split("=")[1])/100)+'℃'
            payload = {'message' : message}
            headers = {'Authorization' : 'Bearer '+ token,}
            r = requests.post(url99,data=payload,headers=headers)
        # データ整形
        for j in range(len(i["sensors"])):
            d = conv(raw.split(";")[j])
            data_dic[i["sensors"][j]] = d
            data_arr.append(str(d))
        data_arr.append(raw)

    # ログファイル出力
    logging(i["sensor_name"], ",".join(data_arr))

# ambient送信処理
for i in range(REPETITIONS):
    try:
        res = am.send(data_dic, timeout=10)
        print('sent to Ambient (ret = %d)' % res.status_code)
        if res.status_code == 200:
            break
    except requests.exceptions.RequestException as e:
        print('request failed: ', e)