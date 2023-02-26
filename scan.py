import socket
import threading
from alive_progress import alive_bar
from pyfiglet import figlet_format
import time


#https://github.com/pwaller/pyfiglet
#https://github.com/rsalmei/alive-progress

#This is a class with an instance variable
#Guidance from https://pynative.com/python-instance-variables/
class PortScanner:
    def __init__(self, host):
        self.host = host
        self.results = []

# This function will pass the user input from the main meunu function and scan the ports, it will return the status of the ports by printing open or closed
# guidence from https://docs.python.org/3/library/socket.html
    def scan(self, port):
        try:
            sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            results=sock.connect_ex((self.host, port))
            sock.close()
            if results == 0:
                print("Port {}: Open".format(port))
                self.results.append("port {}: Open".format(port))
            else:
                # print("Port {}: Closed".format(port))
                self.results.append("port {}: Closed".format(port))
        except:
            print("Unable to connect to host {}".format(self.host))
            self.results.append("Unable to connect to host {}".format(self.host))

#This function will create a list of threads, it will then create a thread for each port (0-1025) and then start each thread and join each thread passing the port number to the scan function
#Guidance from http://pymotw.com/2/threading/ and https://docs.python.org/3/library/threading.html 
    def scanAllPorts(self):
        threads = []
        with alive_bar(65535, title='Scanning') as bar:
            for port in range(1, 65535):
                thread = threading.Thread(target=self.scan, args=(port,))
                threads.append(thread)
                thread.start()
                bar()
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
    
#This function will save the results to a text file    
    def saveResults(self):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        file_name = "Results " + current_time + ".txt"
        with open(file_name, 'w') as f:
            for result in sorted(self.results):
                f.write(result + '\n')
        print(f"Results saved to file '{file_name}'.")

            
#This function will display the menu and call the functions
def main():
    print( figlet_format("Op-scanner", font="big"))
    print("Welcome to the Op-scanner")
    while True:
        print("1. Scan all ports")
        print("2. Scan most vulnerable ports")
        print("3. Save results to file")
        print("4. Exit")
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
            scanner.saveResults()
            break
        elif choice == "4":
            print("Goodbye, See you next time")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()











