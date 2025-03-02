#!/usr/bin/env python3

import schedule
import time

import inky_show

def job():
    inky_show.show()

schedule.every(3).hours.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
