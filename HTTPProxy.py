from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import socket
from CustomProxy import CustomProxy


class MyRequestHandler(BaseHTTPRequestHandler, CustomProxy):
    def do_GET(self):
        # Handle GET requests
        print("headers: " + str(self.headers))

        if self.headers.get("secret-connect"):
            target_address = self.headers["secret-connect"]
            target_address = tuple(target_address.split(":"))
            print("target address:" + str(type(target_address)))
            s = self.try_connect(target_address)
            if not s:
                print("Connection not good!")
                return
            self.send_response(200, 'Connection Established')
            self.end_headers()
            self.connect_relay(s)
            return

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_CONNECT(self):
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
server_address = (IP, int(port))
httpd = ThreadedHTTPServer(server_address, MyRequestHandler)

# Start the server
print(f'Server running on {IP}:{port}')
httpd.serve_forever()
