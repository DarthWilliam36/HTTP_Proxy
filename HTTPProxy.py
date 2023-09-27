import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
from urllib.parse import urlparse
# import requests CANNOT BE USED ON PROXY SERVER

if os.path.isfile(os.path.join(os.getcwd(), 'CustomProxy.py')):
    from CustomProxy import CustomProxy
else:
    raise RuntimeError("CustomProxy.py not found in directory!")


class MyRequestHandler(BaseHTTPRequestHandler, CustomProxy):
    def do_GET(self):
        # Handle Bypass For Network Manager
        if self.headers.get("password") == password or password == "":
            if self.headers.get("secret-connect"):
                target_address = self.headers["secret-connect"]
                target_address = tuple(target_address.split(":"))
                s = self.try_connect(target_address)
                if not s:
                    print("Connection not good!")
                    return
                self.send_response(200, 'Connection Established')
                self.end_headers()
                self.connect_relay(s)
                return

            if self.headers.get("secret-get"):
                resource = self.headers["secret-get"]
                ## IMPLEMENT SENDING GET REQUEST WITH URL
                ## Connect to host
                host = urlparse(resource)
                s = self.try_connect(host, 80)
                #Send get request
                request = f"GET {resource} HTTP/1.1\r\nHost: {host}\r\n\r\n"
                s.sendall(request.encode())
                response = s.recv(65535)
                self.connection.sendall(response)
        else:
            print("Password Rejected!")
            return

    def do_CONNECT(self):
        # Handle Normal Proxy Connection
        print("connecting using CONNECT method")
        if self.headers.get("password") == password or password == "":
            address = self.path.split(':', 1)
            s = self.try_connect(address)
            if not s:
                return
            self.send_response(200, 'Connection Established')
            self.end_headers()
            self.connect_relay(s)


class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    pass


# Create an HTTP server with your custom request handler

IP = input("Enter Server Local IP: ")
port = input("Enter Sever Port: ")
password = input("Enter Access Password (Nothing For No Password: ")
server_address = (IP, int(port))
httpd = ThreadedHTTPServer(server_address, MyRequestHandler)

# Start the server
print(f'Server running on {IP}:{port}')
httpd.serve_forever()
