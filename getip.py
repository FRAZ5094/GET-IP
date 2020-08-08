import requests
import json
import pyfiglet
from time import gmtime,strftime,sleep
import os 

json_file_name="iplog.json"

def get_ip():
	r=requests.get("https://ifconfig.me")
	return r.text
def write_to_json(to_write,file_name):
	with open(file_name, "w") as f:
		json.dump(to_write,f,indent=4)
def read_json(file_name):
	if os.path.exists(file_name):
		with open(file_name,"r") as f:
			iplog=json.load(f)
		return iplog
	else:
		return []

banner=pyfiglet.figlet_format("GET-IP",font="slant")
print(banner)

while True:

	iplog=read_json(json_file_name)
	ip_now=get_ip()

	time_stamp = strftime("%Y-%m-%d %H:%M", gmtime())

	if len(iplog)>0:
		if ip_now==iplog[-1][1]:
			print(f"{time_stamp}: {ip_now}")
		else:
			print(f"{time_stamp}: ip changed from {iplog[-1][1]} to {ip_now}")
			ipchanged=read_json("ipchangedlog.json")
			ipchanged.append(f"{time_stamp}: ip changed from {iplog[-1][1]} to {ip_now}")
			write_to_json(ipchanged,"ipchangedlog.json")

	iplog.append([time_stamp,ip_now])

	write_to_json(iplog,json_file_name)

	sleep(10)
