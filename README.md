# usb_ambient_sender
USBシリーズのデータをambientに送るやつ

# 導入手順
- postfixの追加

  選択肢はLocal only→mail nameは適当

  `sudo apt install -y postfix`

- crontabの設定

  ```
  crontab -e
  ```

  下記を追加

  ```
  */5 * * * * python3 /home/pi/work/usb_ambient_sender/main.py
  ```

# デバッグ
  以下を参照のこと
  - `/var/mail/pi`
  - `/var/log/cron/log`