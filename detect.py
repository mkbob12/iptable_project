import re
from collections import defaultdict
import subprocess
from time import sleep



ip_list = {}
attempts = 5
def ban(auth_log_path):
    with open(auth_log_path, 'r') as file:
        lines = file.readlines() # 여러 줄을 읽은 리스트 객체
        for line in lines :
            pattern =  r"sshd\[\d+\]: Failed password for .* from (\d+\.\d+\.\d+\.\d+) port"
            match = re.search(pattern,line)

            # match.group(0) : 전체 일치 과목
            # match.group(1) : 첫 번째 캡쳐 그룹

            if match: # match가 됐다면
                ip_address = match.group(1)
                if ip_address not in ip_list:
                    ip_list[ip_address] = 0
                ip_list[ip_address] += 1
                print(ip_address)
                pass

        for ip, count in ip_list.items():
            if count >= attempts :
                stop_cmd= f"sudo iptables -A INPUT -s {ip} -j DROP"
                result = subprocess.run([stop_cmd],capture_output=True, text=True,shell=True)
                print(f"{result.stdout} 인 해당 ip를 차단했습니다.")


if __name__ == "__main__":
    auth_log_path = '/var/log/auth.log'

    ban(auth_log_path)