import socket
import threading

#This is a class with an instance variable
#Guidance from https://pynative.com/python-instance-variables/
class PortScanner:
    def __init__(self, host):
        self.host = host

# This function will pass the user input from the main meunu function and scan the ports, it will return the status of the ports by printing open or closed
# guidence from https://docs.python.org/3/library/socket.html
    def scan(self, port):
        try:
            sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            results=sock.connect_ex((self.host, port))
            sock.close()
            if results == 0:
                print("Port {}: Open".format(port))
            else:
                print("Port {}: Closed".format(port))
        except:
            print("Unable to connect to host {}".format(self.host))

#This function will create a list of threads, it will then create a thread for each port (1-1025) and then start each thread and join each thread passing the port number to the scan function
#Guidance from http://pymotw.com/2/threading/ and https://docs.python.org/3/library/threading.html 
    def scanAllPorts(self):
        threads = []
        for port in range(1, 1025):
            thread = threading.Thread(target=self.scan, args=(port,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

#This function will create a list of threads, it will then create a thread for each port (most vulnerable) and then start each thread and join each thread passing the port number to the scan function
#Guideance from http://pymotw.com/2/threading/ and https://docs.python.org/3/library/threading.html and https://blog.netwrix.com/2022/08/04/open-port-vulnerabilities-list
    def scanVulnerablePorts(self):
        ports = [20, 21, 23, 25, 53, 80, 137, 139, 443, 1433, 1434, 3306, 3389, 8080, 8443]
        threads = []
        for port in ports:
            thread = threading.Thread(target=self.scan, args=(port,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
            
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
            scanner = PortScanner(host)
            scanner.scanAllPorts()
        elif choice == "2":
            host = input("Enter host to scan: ")
            scanner = PortScanner(host)
            scanner.scanVulnerablePorts()
        elif choice == "3":
            print("Goodbye, See you next time")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()