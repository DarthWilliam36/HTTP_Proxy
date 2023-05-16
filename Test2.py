from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import select
from OpenSSL import SSL
from OpenSSL.crypto import FILETYPE_PEM, load_certificate, load_privatekey


certificate = load_certificate(FILETYPE_PEM, open(certfile).read())
private_key = load_privatekey(FILETYPE_PEM, open(keyfile).read())


class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Handle GET requests
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Hello, World!')

    def do_CONNECT(self):
        self.connect_relay()

    def connect_relay(self):
        address = self.path.split(':', 1)
        address[1] = int(address[1]) or 443

        self.send_response(200, 'Connection Established')
        self.end_headers()

        context = SSL.Context(SSL.SSLv23_METHOD)
        context.use_certificate(certificate)
        context.use_privatekey(private_key)

        # Create a new SSL connection
        ssl_connection = SSL.Connection(context, self.connection)
        ssl_connection.set_accept_state()

        # Perform the SSL handshake
        try:
            ssl_connection.do_handshake()
        except SSL.Error as e:
            print(f"SSL handshake error: {e}")
            return

        print("SSL Handshake Successful")

        conns = [ssl_connection, socket.create_connection(address, timeout=self.timeout)]
        self.close_connection = False

        while not self.close_connection:
            rlist, wlist, xlist = select.select(conns, [], conns, self.timeout)
            if xlist or not rlist:
                break
            for r in rlist:
                other = conns[1] if r is conns[0] else conns[0]
                data = r.recv(8192)
                if not data:
                    self.close_connection = True
                    print("Connection closed")
                    break
                other.sendall(data)


# Create an HTTP server with your custom request handler
server_address = ('127.0.0.1', 8882)
httpd = HTTPServer(server_address, MyRequestHandler)

# Start the server
print('Server running on http://localhost:8882')
httpd.serve_forever()
