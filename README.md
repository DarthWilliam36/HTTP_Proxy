# HTTPProxy
HTTP Server Proxy made in Python 

This is a simple HTTP Server proxy made in Python that works by responding to the HTTP CONNECT method and establishing a connection between the target server and the client machine.

# TO SET UP
On execution, the script will ask you for you local (private) IP. After entering your IP, enter an open port form the server to run on (usually 80).  

If you are using the proxy on your local network, make sure to set up port forwarding to the server port you set. This will make sure the router will forward any incoming packets to your device.  

For any other questions, feel free to email <a href="https://mail.google.com/mail/u/1/#inbox?compose=new">williamcodez@gmail.com</a>  

# FILE DESCRIPTIONS
The ```HTTPProxy.py``` file is the main proxy file for the server. This will recive requests and return the appropriate packets to sustian an HTTP connection.  
The ```Client.py``` file is an experimental packet editor that is used to bypass network security managers.  
The ```CustomProxy.py``` file contains the proxy class used for the ```HTTPProxy.py``` and ```Client.py``` files.



