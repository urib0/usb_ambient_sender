#!/usr/bin/env python3
# python3.7で動作確認済み

import serial
import ambient
import time
import json
import datetime
import random
import os

DEBUG = True


def logging(name, data):
    filename = name + "_" + datetime.datetime.now().strftime("%Y-%m-%d") + ".csv"
    timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    write_str = timestamp + "," + data
    path = "./" + conf["logdir"] + "/" + name + "/"

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
f = open("./config.json", "r")
conf = json.loads(f.read())
f.close()

am = ambient.Ambient(conf["ambient_channel"], conf["ambient_key_write"])

while 1:
    data_dic = {}
    for i in conf["devices"]:
        # シリアル読み込み
        readSer = serial.Serial(i["serial_port"], i["serial_rate"], timeout=3)
        raw = readSer.readline().decode().replace('\n', '')
        readSer.close()

        # データ整形
        data_arr = []
        for j in range(len(i["sensors"])):
            d = conv(raw.split(";")[j])
            data_dic[i["sensors"][j]] = d
            data_arr.append(str(d))

        # ログファイル出力
        data_arr.append(raw)
        logging(i["sensor_name"], ",".join(data_arr))

    # ambient送信処理
    res = am.send(data_dic, timeout=60)
    if 200 != res.status_code:
        time.sleep(random.randint(1, 10))
        res = am.send(data_dic, timeout=60)

    # 送信周期待ち
    time.sleep(conf["interval"])
