# debug
#from dotenv import load_dotenv
#load_dotenv()

import serial
import ambient
import time
import datetime
import os
import sys
import re
import requests

# Get environment variables
SERIAL_PORT=os.getenv('SERIAL_PORT')
AMBIENT_CHANNEL=os.getenv('AMBIENT_CHANNEL')
AMBIENT_KEY_WRITE=os.getenv('AMBIENT_KEY_WRITE')
SERIAL_RATE=os.getenv('SERIAL_RATE')
INTERVAL=os.getenv('INTERVAL')


def main():
    am = ambient.Ambient(AMBIENT_CHANNEL, AMBIENT_KEY_WRITE)

    while True:
        # Read serial port
        try:
            readSer = serial.Serial(SERIAL_PORT, SERIAL_RATE, timeout=3)
        except serial.serialutil.SerialException as e:
            print(e, file=sys.stderr)
        raw = readSer.readline().decode()
        readSer.close()

        # Sent co2 data to ambient
        co2 = int(re.match(r'co2=([0-9]+);', raw).groups()[0])
        data = {"d1": co2}
        try:
            res = am.send(data, timeout=10)
            res.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(e, file=sys.stderr)
        else:
            print('Send Data: StatusCode={}, Data={}'.format(res.status_code, data), file=sys.stdout)

        time.sleep(int(INTERVAL))


if __name__ == "__main__":
    main()
