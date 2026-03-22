# my-inky

Raspberry Pi + Pimoroni Inky Impression 5.7" カラー電子ペーパーに天気・カレンダーなどの情報を表示する自宅用ダッシュボード。

![Image](https://github.com/user-attachments/assets/4c9bda24-5f26-44ee-b218-cb1cb946e322)

## ハードウェア

- [Pimoroni Inky Impression 5.7"](https://shop.pimoroni.com/products/inky-impression-5-7?variant=32298701324371)（7色カラー電子ペーパー、600×448px）
- Raspberry Pi Zero 2W（2.4GHz Wi-Fi のみ対応）

## 機能

### ページ一覧

ボタンでページを切り替えて表示します。

| ボタン | ページ | 内容 |
|---|---|---|
| A | 天気 | 現在の気温・湿度・気圧・天気アイコン＋48時間の降水確率・気温グラフ |
| B | 日付 | 日付・曜日・日の出/日の入り時刻・月の満ち欠け・次の満月日 |
| C | カレンダー | 月間カレンダー（日曜=赤・土曜=青・祝日=橙・今日=赤丸） |
| D | 写真 | `photos/` ディレクトリの写真をランダム表示 |

同じボタンを再押しすると現在のページを更新します。

### 自動更新

3時間ごとに現在のページを自動再描画します。

## セットアップ

### 1. リポジトリのクローン

```bash
git clone git@github.com:<username>/inky.git ~/my_inky
cd ~/my_inky
```

### 2. 依存ライブラリのインストール

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

> Raspberry Pi の場合、`python3-dev` が必要なことがあります。
> ```bash
> sudo apt install -y python3-dev
> ```

### 3. SPI 設定（Raspberry Pi）

```bash
# /boot/firmware/config.txt に追記
echo "dtoverlay=spi0-0cs" | sudo tee -a /boot/firmware/config.txt
sudo reboot
```

### 4. 環境変数の設定

[OpenWeatherMap](https://openweathermap.org/) でAPIキーを取得し、設定します。

```bash
echo 'export OPENWEATHER_API_KEY=your_api_key_here' >> ~/.bashrc
source ~/.bashrc
```

### 5. 起動

```bash
source venv/bin/activate
python inky_schedule.py
```

### 6. 自動起動（systemd）

```bash
sudo nano /etc/systemd/system/inky.service
```

```ini
[Unit]
Description=Inky Display
After=network-online.target
Wants=network-online.target

[Service]
User=<username>
WorkingDirectory=/home/<username>/my_inky
Environment=OPENWEATHER_API_KEY=your_api_key_here
ExecStart=/home/<username>/my_inky/venv/bin/python inky_schedule.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable inky
sudo systemctl start inky
```

## Mac での動作確認

```bash
source inky_venv/bin/activate
export OPENWEATHER_API_KEY=your_api_key_here

python preview.py           # 全ページを確認
python preview.py weather   # 指定ページのみ確認
python preview.py date
python preview.py cal
python preview.py photo
```

実行すると `preview_<page名>.png` として保存されます。

## 写真の追加

`photos/` ディレクトリに `.jpg` / `.png` を入れるだけです。アスペクト比が異なる場合は黒の余白（レターボックス）が付きます。

```bash
cp your_photo.jpg ~/my_inky/photos/
```

## プロジェクト構成

```
my_inky/
├── pages/
│   ├── __init__.py     # ページ一覧
│   ├── weather.py      # 天気ページ
│   ├── date.py         # 日付・天文ページ
│   ├── cal.py          # カレンダーページ
│   └── photo.py        # 写真ページ
├── photos/             # 表示する写真を入れるディレクトリ
├── preview.py          # Mac確認用
├── inky_show.py        # ページ管理・ボタン制御
├── inky_schedule.py    # エントリーポイント（自動更新）
├── weather_api.py      # OpenWeatherMap API
├── weathericons-regular-webfont.ttf
└── requirements.txt
```

## 参考

- [Weather Icons](https://erikflowers.github.io/weather-icons/)
- [OpenWeatherMap Current API](https://openweathermap.org/current)
- [OpenWeatherMap Forecast API](https://openweathermap.org/forecast5)
- https://nobo-san.com/inky-impression-4/
- https://nobo-san.com/weather-calendar/
- https://kotamorishita.com/rpi-epaper-weather-station/
