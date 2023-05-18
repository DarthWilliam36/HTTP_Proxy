from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import socket
import select


class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Handle GET requests
        print("headers: " + str(self.headers))

        if self.headers.get("secret-connect"):
            target_address = self.headers["secret-connect"]
            self.connect_relay(target_address)
            return

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_CONNECT(self):
        address = self.path.split(':', 1)
        self.connect_relay(address)

    def connect_relay(self, target_address):
        try:
            s = socket.create_connection(target_address, timeout=self.timeout)
        except:
            self.send_error(502)
            return

        self.send_response(200, 'Connection Established')
        self.end_headers()

        conns = [self.connection, s]
        self.close_connection = False

        print("New Connection: " + str(self.connection.getpeername()))

        while not self.close_connection:
            rlist, wlist, xlist = select.select(conns, [], conns, self.timeout)
            if xlist or not rlist:
                break
            for r in rlist:
                other = conns[1] if r is conns[0] else conns[0]
                data = r.recv(65535)
                if not data:
                    self.close_connection = True
                    print("Broke Connection: " + str(self.connection.getpeername()))
                    break
                other.sendall(data)


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
