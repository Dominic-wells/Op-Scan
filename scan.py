import socket

def scan(ip, port):
    try:
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        results=sock.connect_ex((ip, port))
        if results == 0:
            print ("Port {}: Open".format(port))
        else:
            print ("Port {}: Closed".format(port))
        sock.close()
    except:
        print("unable to connect to host {}".format(ip))

host = input("Enter host to scan: ")
for port in range(1,1025):
    scan(host, port)