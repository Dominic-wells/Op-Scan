import socket

class PortScanner:
    def __init__(self, host):
        self.host = host

# This function will scan the port and return the status of the ports 1,1025 (open or closed)
# guidence from https://docs.python.org/3/library/socket.html
    def scan(self, port):
        try:
            sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            results=sock.connect_ex((self.host, port))
            if results == 0:
                print ("Port {}: Open".format(port))
            else:
                print ("Port {}: Closed".format(port))
            sock.close()
        except:
            print("Unable to connect to host {}".format(self.host))

#Function 2 will scan the most vulnerable ports and return the status of the
#ports 20,21,23,25,53,80,137,139,443,1433,1434,3306,3389,8080,8443 (open or closed)
#guidence from https://blog.netwrix.com/2022/08/04/open-port-vulnerabilities-list/#:~:text=Ports%2080%2C%20443%2C%208080%20and,request%20forgeries%20and%20DDoS%20attacks.   
#This function will display the menu and call the functions
def main():
    print("Welcome to the Op-scanner")
    while True:
        print("1. Scan all ports")
        print("2. Scan most vulnerable ports")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            host = input("Enter host to scan: ")
            for port in range(1, 1025):
                scanner = PortScanner(host)
                scanner.scan(port)
        elif choice == "2":
            host = input("Enter host to scan: ")
            ports = [20, 21, 23, 25, 53, 80, 137, 139, 443, 1433, 1434, 3306, 3389, 8080, 8443]
            for port in ports:
                scanner = PortScanner(host)
                scanner.scan(port)
        elif choice == "3":
            print("Goodbye, See you next time")
            break
        else:
            print("Invalid choice")
            
#This will call the main function when the program is run
if __name__ == "__main__":
    main()