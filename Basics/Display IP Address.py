#Displays current IP address

#clear the screen
import os
os.system('clear')

#get the IP address
import socket
ipaddress = socket.gethostbyname(socket.gethostname())
fqdn = socket.gethostbyname(socket.getfqdn())

print(fqdn)

print('Your IP address: ' + ipaddress)


