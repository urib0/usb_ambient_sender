#!/usr/bin/env python3
# python3.7で動作確認済み

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
    if data[0] in {"temp","hum"}:
        return int(data[1]) / 100
    else:
        return int(data[1])


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
        try:
            f = open(filename,"r")
            # ログの末尾1行をとってくる
            lines = f.readlines()[-1:][0][:-1]
            f.close

            # ログに含まれるセンサの数がconfig.jsonと同じか確認
            data_list = lines.split(",")[1].split(";")
            data_num = (len(data_list) - 1)
            for i in range(data_num):
                # センサ名と数字のペアができる ex) ["temp","2657"]
                data_pair = data_list[i].split("=")

                if data_pair[0] in device["sensors"]:
                    # 送信すべきambientのデータ番号が存在することを確認 ex) d1~d8
                    data_dic[device["sensors"][data_pair[0]]] = conv(data_pair)
                else:
                    break
        except Exception as e:
            print(e)
            pass

# ambient送信処理
for i in range(REPETITIONS):
    try:
        res = am.send(data_dic, timeout=3)
        print('sent to Ambient (ret = %d)' % res.status_code)
        if res.status_code == 200:
            break
        time.sleep(random.randint(1,10))
    except requests.exceptions.RequestException as e:
        print('request failed: ', e)
