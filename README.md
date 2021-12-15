# usb_ambient_sender
USBシリーズのデータをambientに送るやつ

# 導入手順
- ambientモジュールの追加
  ```
  pip3 install git+https://github.com/AmbientDataInc/ambient-python-lib.git
  ```

- postfixの追加

  選択肢はLocal only→mail nameは適当

  ```
  sudo apt install -y postfix
  ```

- crontabのログ出力を有効化

  `/etc/rsyslog.conf`の以下のコメントアウトを外す

  ```
  cron.*                          /var/log/cron.log
  ```

- crontabの設定

  `crontab -e`で下記を追加

  ```
  */5 * * * * python3 /home/pi/work/usb_ambient_sender/main.py
  ```

# デバッグ
  以下を参照のこと
  - `/var/mail/pi`
  - `/var/log/cron/log`
