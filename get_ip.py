import requests
import pyfiglet
import os
import pandas as pd
from time import gmtime, strftime, sleep
log_file_name = "IP_log.csv"
sleep_time = 60

sleep_time *= 60


def read_file():
    if os.path.exists(log_file_name):
        data = pd.read_csv(log_file_name, header=0)
        return data
    else:
        return pd.DataFrame([], columns=["Time_Stamp", "IP"])


def get_ip():
    r = requests.get("https://ifconfig.me")
    if r.ok:
        return r.text
    else:
        return "error"


def write_to_file(to_write):

    with open(log_file_name, "a") as f:
        f.write(to_write+"\n")


if __name__ == "__main__":
    banner = pyfiglet.figlet_format("GET-IP", font="slant")
    print(banner)

    while True:
        ip_now = get_ip()
        data = read_file()
        if len(data) > 0:
            last_row = data.iloc[-1:, :].values[0]
            last_ip = last_row[1]
            if last_ip != "nofile" and last_ip != ip_now:
                print(f"IP changed from {last_ip} to {ip_now}")

        time_stamp = strftime("%Y-%m-%d %H:%M", gmtime())
        print(f"{time_stamp} : {ip_now}")
        new_row = {"Time_Stamp": time_stamp, "IP": ip_now}
        to_write = data.append(new_row, ignore_index=True)
        to_write.to_csv(log_file_name, index=False)
        sleep(sleep_time)
