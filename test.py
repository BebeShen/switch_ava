import paramiko
import requests
import datetime
import json
import os
from dotenv import load_dotenv

load_dotenv()
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())    

bmc_check_list = [
    "10.30.3.68",
    "10.30.3.69",
    "10.30.3.70",
    "10.30.3.71",
    "10.30.3.72",
    "10.30.3.73"
]

for s in bmc_check_list:
    try:
        client.connect(hostname=s, port=22, username="root", password="onl", timeout=5)
        stdin, stdout, stderr = client.exec_command("curl http://[fe80::ff:fe00:1%usb0]:8080/api/sys/bmc")
        print(stdout)
        stdout_output = stdout.read().decode().strip()
        stderr_output = stderr.read().decode().strip()
        print("Error:", stderr_output)
        print("stdout:", stdout_output)

        print(json.dumps(json.loads(stdout_output), indent=4))
    except Exception as e:
        print(e)