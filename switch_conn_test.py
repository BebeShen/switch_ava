import paramiko
import requests
import datetime
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
        client.connect(ip, port, user, psw, timeout=5)
        if ip in bmc_check_list:
            stdin, stdout, stderr = client.exec_command("curl http://[fe80::ff:fe00:1%usb0]:8080/api/sys/bmc")
            
            # read stdout/stderr
            stdout_output = stdout.read().decode().strip()
            stderr_output = stderr.read().decode().strip()

            if str(stdout.channel.recv_exit_status()) == "6":
                print("[-] Connection Failed : Could not resolve host.")
                return False, "Connection Failed : Could not resolve host."
            elif str(stdout.channel.recv_exit_status()) == "7":
                print("[-] Connection Failed : Connection refused.")
                return False, "Connection Failed : Connection refused."
            else:
                print("[+] Connection Success!")
                print(json.dumps(json.loads(stdout_output), indent=4))
                return True, None
        else:
            print("[+] Connection Success!")
            return True, None
    except paramiko.SSHException as e:
        print(f"[-] SSH connection error: {e}")
        return False, e
    except Exception as e:
        print(f"[-] Unexpected error: {e}")
        return False, e

def line_notify(msg):
    url = 'https://notify-api.line.me/api/notify'
    token = os.getenv('SECRET')
    # 設定權杖
    headers = {
        'Authorization': 'Bearer ' + token    
    }
    # 發送的訊息
    message = '\n'.join(msg)
    print(message)
    data = {
        'message':'\n'+message     
    }
    # 使用 POST 方法
    data = requests.post(url, headers=headers, data=data)   

def main():
    message = []

    now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
    print(now)
    message.append(now)
    # switch
    for s in bmc_check_list:
        result, msg = check_ssh(s, user="root", psw=os.getenv('PSW_NEW'))
        if result:
            message.append("[+] Switch[{}] is UP!".format(s))
        else:
            message.append("[-] Switch[{}] is DOWN! \n[-] {}".format(s, msg))

    # 73 bmc
    result, msg = check_ssh("10.30.3.76", user="root", psw=os.getenv('PSW_BMC'))
    if result:
        message.append("[+] BMC(73) 10.30.3.76 is UP!")
    else :
        message.append("[-] BMC(73) 10.30.3.76 is DOWN!\n[-] {}".format(msg))
    # server
    result, msg = check_ssh("10.30.3.75", user="root", psw=os.getenv('PSW_SERVER'))
    if result:
        message.append("[+] Server[10.30.3.75] is UP!")
    else :
        message.append("[-] Server[10.30.3.75] is DOWN!")
    
    line_notify(message)


if __name__ == '__main__':
    main()
