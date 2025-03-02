#!/usr/bin/env python3

import schedule
import time

import inky_show

def job():
    inky_show.show()

#1分毎のjob実行を登録
schedule.every(1).minutes.do(job)

# schedule.every(3).hours.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
