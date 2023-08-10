# iptable_project
지속적으로 공격하는 ip 주소를 log를 통하여 ip 주소 허용 및 차단 하는 코드 간단 구현 


# detect.py 
공격자 가 우분투 서버에 ssh 를 bruteforce 시도하는 것을 /var/log/auth.log 파일을 바라보며 감지하다가 5회 이상 접속에 실패하면
iptables 정책을 통해서 사용자 ( ip 주소 기반 ) 의 접속을 차단한다. 

# accept.py 
공격자의 공격 중 최근 1분 동안의 로그만을 보고 5회 이상 실패한 경우 해당 사용자를 차단한 후 5분이 지나면 차단을 해제한다. 
