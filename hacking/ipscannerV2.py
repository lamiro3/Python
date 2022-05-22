#-*-coding: utf-8-*-
import netaddr
import pyping
import threading

print("._____________    _________                                         ")
print("|   \______   \  /   _____/ ____ _____    ____   ____   ___________ ")
print("|   ||     ___/  \_____  \_/ ___\\__  \  /    \ /    \_/ __ \_  __ \ ")
print("|   ||    |      /        \  \___ / __ \|   |  \   |  \  ___/|  | \/")
print("|___||____|     /_______  /\___  >____  /___|  /___|  /\___  >__|   ")
print("                        \/     \/     \/     \/     \/     \/       ")
print("                                                         (V : 0.0.2)")
print("____________________________________________________________________")
print("|                                                                  |")
print("|----------------------Making-by-r00t@lam1r0-----------------------|")
print("|                                                                  |")
print("|             -h > help, -s > IPscan, -b > quit/back               |")
print("|                   Email(kktthh4076@gmail.com)                    |")
print("|__________________________________________________________________|")

ThreadLock = threading.Lock()
threads = []
while True:

    talk = str(input("IP_Scanner@~/  "))

    if talk == "-h":
        print("명령형식 => ***.***.***.0/24(가장자리에 큰따움표 추가)")
    elif talk == "-s":
        print("스캔할 주소를 입력하십시오. [형식 => ***.***.***.0/24] ")
        while True:
            print("  ")
            print("  ")
            print("  ")
            print("  ")
            print("  ")
            print("  ")
            print("  ")
            print("  ")
            print("  ")
            print("  ")
            print("  ")
            print("  ")
            print("  ")
            print("  ")
            print("  ")
            print("  ")
            print("  ")
            print("  ")
            print("  ")
            print("  ")
            print("  ")
            print("  ")
            print("  ")
            print("  ")
            print("  _________                     ")
            print(" /   _____/ ____ _____    ____  ")
            print(" \_____  \_/ ___\\__  \  /    \ ")
            print(" /        \  \___ / __ \|   |  \ ")
            print("/_______  /\___  >____  /___|  /")
            print("        \/     \/     \/     \/ ")
            print("____________________________________________________________________")
            print("|                                                                  |")
            print("|----------------------Making-by-r00t@lam1r0-----------------------|")
            print("|                                                                  |")
            print("|                       -b > back to home                          |")
            print("|                   Email(kktthh4076@gmail.com)                    |")
            print("|__________________________________________________________________|")


            IPlist = str(input("IP_Scanner/AliveIPscan@~/  "))
            if IPlist == "-b":
                break        
            def IPscan(ip):
                try:
                    if not pyping.ping(str(ip)).ret_code:
                        ThreadLock.acquire()
                        print("Alive HostAddress >>>    ") + str(ip)
                        ThreadLock.release()
                except:
                    pass
            for ip in netaddr.IPNetwork(IPlist):
                ip = str(ip)
                th = threading.Thread(target=IPscan,args=(ip,))
                th.start()
                threads.append(th)

            for t in threads:
                t.join()

            print("Scanning is End..")

            IPscan(IPlist)

    elif talk == "-b":
        print("Bye~~%")
        break
    else:
        print("알수없는 명령형식입니다. 재입력해주시기 바랍니다.")
