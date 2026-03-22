import threading
import time

import pages

# ボタンのGPIOピン番号 (A, B, C, D)
# Raspberry Pi 5 は gpiochip4、Pi 4/Zero は gpiochip0
BUTTONS = [5, 6, 16, 24]
LABELS = ["A", "B", "C", "D"]
GPIO_CHIP = "/dev/gpiochip4"

DEBOUNCE_SEC = 0.5

_inky = None
_current_page = 0
_last_button_time = 0
_lock = threading.Lock()


def _get_inky():
    global _inky
    if _inky is None:
        from inky.auto import auto
        _inky = auto(ask_user=True, verbose=True)
    return _inky


def _show_page(index):
    global _current_page
    _current_page = index % len(pages.PAGES)
    img = pages.PAGES[_current_page].create_image()
    inky = _get_inky()
    inky.set_image(img)
    inky.show()


def show():
    """現在のページを再描画する（スケジューラから呼ばれる）"""
    with _lock:
        _show_page(_current_page)


def _handle_buttons():
    """ボタン押下を監視するループ（別スレッドで動作）"""
    global _last_button_time

    try:
        import gpiod
        from gpiod.line import Direction, Bias, Edge
    except ImportError:
        print("gpiod not available, button handling disabled")
        return

    try:
        with gpiod.request_lines(
            GPIO_CHIP,
            consumer="inky-buttons",
            config={
                tuple(BUTTONS): gpiod.LineSettings(
                    direction=Direction.INPUT,
                    bias=Bias.PULL_UP,
                    edge_detection=Edge.FALLING,
                )
            },
        ) as request:
            while True:
                for event in request.read_edge_events():
                    now = time.time()
                    if now - _last_button_time < DEBOUNCE_SEC:
                        continue
                    _last_button_time = now

                    idx = BUTTONS.index(event.line_offset)
                    label = LABELS[idx]
                    print(f"Button {label} pressed")

                    with _lock:
                        if idx == 0:    # A: 前のページ
                            _show_page(_current_page - 1)
                        elif idx == 1:  # B: 次のページ
                            _show_page(_current_page + 1)
                        elif idx == 2:  # C: 現在のページを更新
                            _show_page(_current_page)
                        # D (idx==3): 予約
    except Exception as e:
        print(f"Button handling error: {e}")


def start():
    """ボタン監視とスケジューラを起動する（ラズパイ用エントリーポイント）"""
    import schedule

    btn_thread = threading.Thread(target=_handle_buttons, daemon=True)
    btn_thread.start()

    schedule.every(3).hours.do(show)

    with _lock:
        _show_page(0)

    while True:
        schedule.run_pending()
        time.sleep(1)
