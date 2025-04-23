import time
import schedule
import subprocess
import os

def run_scrapy():

    try:
        subprocess.run(["python", "main.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error has occurred: {e}")

#
schedule.every(2).hours.do(run_scrapy)
while True:
    schedule.run_pending()
    time.sleep(60)
