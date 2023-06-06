# HTTPProxy
Python-based HTTP Server Proxy designed to bypass network managers that restrict or block services.

# SET UP SERVER 
On the server you can run:
```
sudo python HTTPProxy.py
```
The script will then ask you for you local (private) IP. After entering your IP, enter an open port for the server to run on (usually 80).

If you are using the proxy on your local network, make sure to set up port forwarding to the server port you set. This will make sure the router will forward any incoming packets to your device.  

This is now a functioning network proxy on its own but is not able to bypass a network manager. Use the ```Client.py``` script on your local machine to allow this service. 

# SET UP CLIENT
Before you run this script, you must change the ```proxy_address``` to your servers IP address and ```local_port``` to any port you want, also change ```password``` if nececary. In my case, I needed a domain name in order to properly connect to my server inside the restricted network. This was because they block any connection to a direct IP address. After these steps, run the client with:
```
sudo python Client.py
```
Make sure to change you browser settings to connect to your local proxy (127.0.0.1 with the local port you chose).

# FILE DESCRIPTIONS
The ```HTTPProxy.py``` file is the main proxy file for the server. This will recive requests and return the appropriate packets to sustian an HTTP connection.   
  
The ```Client.py``` file is a packet editor that is used to bypass network security managers.    
  
The ```CustomProxy.py``` file contains the proxy class used for the ```HTTPProxy.py``` and ```Client.py``` files.  



