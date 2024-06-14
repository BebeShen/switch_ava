import paramiko
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

bmc_check_list = [
    "10.30.3.68",
    "10.30.3.69",
    "10.30.3.70",
    "10.30.3.71",
    "10.30.3.72",
    "10.30.3.73"
]

def check_ssh(ip, user, psw):
    port = 22
    print("[+] Checking {} ...".format(ip))
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(ip, port, user, psw)
        print("[+] Connection Success!")
        if ip in bmc_check_list:
            stdin, stdout, stderr = client.exec_command("curl http://[fe80::ff:fe00:1%usb0]:8080/api/sys/bmc")
            result = stdout.readlines()[0]
            print(json.dumps(json.loads(result), indent=4))
        return True
    except Exception as e:
        print("[-] Connection Fail!")
        print("========================")
        print(e)
        print("========================")
        return False

def line_notify():
    url = 'https://notify-api.line.me/api/notify'
    token = os.getenv('SECRET')
    # 設定權杖
    headers = {
        'Authorization': 'Bearer ' + token    
    }
    # 發送的訊息
    data = {
        'message':'測試一下！\n換行'     
    }
    # 使用 POST 方法
    data = requests.post(url, headers=headers, data=data)   

def main():
    # switch
    check_ssh("10.30.3.68", user="root", psw=os.getenv('PSW_OLD'))
    check_ssh("10.30.3.69", user="root", psw=os.getenv('PSW_NEW'))
    check_ssh("10.30.3.70", user="root", psw=os.getenv('PSW_NEW'))
    check_ssh("10.30.3.71", user="root", psw=os.getenv('PSW_NEW'))
    check_ssh("10.30.3.72", user="root", psw=os.getenv('PSW_NEW'))
    check_ssh("10.30.3.73", user="root", psw=os.getenv('PSW_NEW'))
    # 73 bmc
    if check_ssh("10.30.3.76", user="root", psw=os.getenv('PSW_BMC')) :
        print("73 bmc UP")
    else :
        print("73 bmc DOWN")
    # server
    check_ssh("10.30.3.75", user="root", psw=os.getenv('PSW_SERVER'))


if __name__ == '__main__':
    line_notify()
    # main()
