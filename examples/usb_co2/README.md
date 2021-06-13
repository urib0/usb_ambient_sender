# usb_co2をつないだRaspberryPiからAmbientにデータを送るやつ

注意: Docker Desktop for Mac だとこれのDocker版は動かない。HyperKitがホストのUSBデバイスを認識できないのが原因っぽいので、VirtualBoxとかで動かせばなんとかなるかも。

## Requirements

- docker
- docker-compose

## Usage

### 接続されているデバイスファイルを確認する

```
ls /dev/tty*
...
/dev/ttyAMA0
...
```

### docker-compose.yaml を書き換える

次の３つを自分の環境に合わせて書き換える

- デバイスファイル名
- 環境変数 `AMBIENT_CHANNEL`
- 環境変数 `AMBIENT_KEY_WRITE`

## 起動

```
docker-compose up -d
```

## 停止

```
docker-compose down
```

## ログの確認

```
docker-compose logs -t
Attaching to usb_co2_sender_1
sender_1  | 2021-06-13T09:44:08.510642072Z Send Data: StatusCode=200, Data={'d1': 1777}
sender_1  | 2021-06-13T09:49:09.215577481Z Send Data: StatusCode=200, Data={'d1': 1749}
sender_1  | 2021-06-13T09:54:09.849074239Z Send Data: StatusCode=200, Data={'d1': 762}
sender_1  | 2021-06-13T09:59:10.510990781Z Send Data: StatusCode=200, Data={'d1': 568}
sender_1  | 2021-06-13T10:04:11.161788626Z Send Data: StatusCode=200, Data={'d1': 497}
sender_1  | 2021-06-13T10:09:11.813550667Z Send Data: StatusCode=200, Data={'d1': 467}
...
```