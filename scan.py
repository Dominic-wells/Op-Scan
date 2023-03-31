#This will try to import the modules needed for the program to run, if it fails it will print an error message and exit the program.
#Guidance from https://blog.airbrake.io/blog/python/importerror-and-modulenotfounderror
try:
    import socket
    import threading
    from alive_progress import alive_bar
    from pyfiglet import figlet_format
    import time
    import whois
    from port_to_service import port_to_service
except ImportError as e:
    if e.name == 'port_to_service':
        print("The 'port_to_service' dictionary is not installed, make sure to download that also.")
    else:
        print(f"Missing module: {e.name}")
        print("Please install the module using `pip install <module_name>`")
    exit(1)


#This is a class with an instance variable
#Guidance from https://pynative.com/python-instance-variables/
class PortScanner:
    def __init__(self, host):
        self.host = host
        self.results = []


#This function will pass the user input from the main meunu function and scan the ports, 
#it will return the status of the ports by printing open or closed as well as the service running on the port if it is open by importing a dictionary from Port_to_service that holds common values.
#guidence from https://docs.python.org/3/library/socket.html
    def scan(self, port, bar=None):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((self.host, port))
            sock.close()
            if result == 0:
                service = port_to_service.get(port, 'Unknown')
                print(f"Port {port}: {service} is open")
                self.results.append(f"Port {port}: {service} is open")
            else:
                self.results.append(f"Port {port}: Closed")
            if bar:
                bar()
        except:
            print(f"Unable to connect to host {self.host}")
            self.results.append(f"Unable to connect to host {self.host}")


#This function will create a list of threads, it will then create a thread for each port (0-1025) and then start each thread and join each thread passing the port number to the scan function
#Guidance from http://pymotw.com/2/threading/ and https://docs.python.org/3/library/threading.html 
    def scanAllPorts(self):
        threads = []
        with alive_bar(65535, title='Scanning') as bar:
            for port in range(1, 65535):
                thread = threading.Thread(target=self.scan, args=(port, bar))
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


#This function will perform a DNS lookup on the host and return the IP address.    
    def dns_lookup(self):
        try:
            ip_address = socket.gethostbyname(self.host)
            print(f"{self.host} resolved to {ip_address}")
        except socket.gaierror:
            print(f"Could not resolve {self.host}")


#This function will perform a WHOIS lookup on the host and return the domain name, registrar, creation date expiration date , status, emails, orgName, orgAddress, orgCity and postalCode.
    def whois_lookup(self):
        try:
            domain_info = whois.whois(self.host)
            print(f"Domain name: {domain_info.name}")
            print(f"Registrar: {domain_info.registrar}")
            print(f"Creation date: {domain_info.creation_date}")
            print(f"Expiration date: {domain_info.expiration_date}")
            print(f"Status: {domain_info.status}")
            print(f"Emails: {domain_info.emails}")
            print(f"orgName: {domain_info.orgName}")
            print(f"orgAddress: {domain_info.orgAddress}")
            print(f"orgCity: {domain_info.orgCity}")
            print(f"postalCode: {domain_info.postalCode}")
        except whois.exceptions.WhoisLookupError:
            print(f"Could not perform WHOIS lookup for {self.host}")


#This function will save the results to a text file with the current date and time and in order of open and closed ports in port number order
#guidance for lambda sorting from https://sparkbyexamples.com/python/sort-using-lambda-in-python/ , https://www.freecodecamp.org/news/the-string-strip-method-in-python-explained/ 
#and https://stackoverflow.com/questions/17474211/how-to-sort-python-list-of-strings-of-numbers
    def saveResults(self):
        current_time = time.strftime("%Y-%m-%d--%H-%M-%S", time.gmtime())
        file_name = f"{self.host}-Results-{current_time}.txt"
        open_ports = []
        closed_ports = []
        for result in self.results:
            if 'open' in result:
                open_ports.append(result)
            else:
                closed_ports.append(result)
        with open(file_name, 'w') as f:
            f.write("Open ports:\n")
            for result in sorted(open_ports, key=lambda x: int(x.split()[1].rstrip(':'))):
                f.write(result + '\n')
            f.write("\nClosed ports:\n")
            for result in sorted(closed_ports, key=lambda x: int(x.split()[1].rstrip(':'))):
                f.write(result + '\n')


#This function will display the menu and call the functions ready for the user to select an option, added error handling for saving scan without performing a scan first.
def main():
    print('\n' * 2)
    print( figlet_format("Op-scanner", font="big"))
    print("Welcome to the Op-scanner")
    scanner = None 
    while True:
        print()
        print(u'\u2500' * 30)
        print("1. Scan all ports")
        print("2. Scan most vulnerable ports")
        print("3. Save results to file")
        print("4. Perform DNS lookup")
        print("5. Perform WHOIS lookup")
        print("6. Exit")
        print(u'\u2500' * 30)
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
            if scanner:
                scanner.saveResults()
            else:
                print("No results to save. Please run a scan first.")
        elif choice == "4":
            host = input("Enter host to perform DNS lookup: ")
            scanner = PortScanner(host)
            scanner.dns_lookup()
        elif choice == "5":
            host = input("Enter domain to lookup: ")
            scanner = PortScanner(host)
            scanner.whois_lookup()    
        elif choice == "6":
            print("Goodbye, See you next time")
            break
        else:
            print("Invalid choice...")
            
if __name__ == "__main__":
    main()