
import re
from collections import defaultdict
import subprocess
import time
from datetime import datetime


ip_list = {}
attempts = 5 

def log_file(auth_log_path):
    with open(auth_log_path, 'r') as file:
        lines = file.readlines() # 여러 줄을 읽은 리스트 객체 
        for line in lines :
            
            match = re.search(r"sshd.+Failed password for.+from (\d+\.\d+\.\d+\.\d+)", line)
            
            # match.group(0) : 전체 일치 과목 
            # match.group(1) : 첫 번째 캡쳐 그룹 
            
            if match: # match가 됐다면 
             
                ip_address = match.group(1)

                # 요일과 시간을 추출
                log_time = line.split()[0] + " " + line.split()[1] + " " + datetime.now().strftime("%Y") + " " + line.split()[2]
                
                log_time_obj = datetime.strptime(log_time, "%b %d %Y %H:%M:%S")
                
                current_time = datetime.now()
                time_differnece = current_time - log_time_obj
                if time_differnece.total_seconds()  < 60:
                    ban(ip_address)

                    
def ban(ip_address):
    if ip_address not in ip_list:
        ip_list[ip_address] = 0   
       
    ip_list[ip_address] += 1 
    print(ip_address)
               
    
                    
def unban(ip_address):
    delete_cmd= f"sudo iptables -F"
    result = subprocess.run([delete_cmd],capture_output=True, text=True,shell=True)
    accept_cmd= f"sudo iptables -A INPUT -s {ip_address} -j ACCEPT"
    result = subprocess.run([accept_cmd],capture_output=True, text=True,shell=True)
    print(f"{result.stdout} 인 해당 ip를 허용했습니다.")
    
    

if __name__ == "__main__":
    auth_log_path = '/var/log/auth.log'
    #auth_log_path = './auth.log'
    log_file(auth_log_path)
   
    for ip, count in ip_list.items():
        
        if count >= attempts:
            stop_cmd= f"sudo iptables -A INPUT -s {ip} -j DROP"
            result = subprocess.run([stop_cmd],capture_output=True, text=True,shell=True)
            print(f"{result.stdout} 인 해당 ip를 차단했습니다.")
            time.sleep(300)
            unban(ip)

      

    

