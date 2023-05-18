from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import socket
import select

proxy_address = ("52.23.193.65", 80)


class MyRequestHandler(BaseHTTPRequestHandler):
    def do_CONNECT(self):
        print("Incoming CONNECT packet:")
        print(self.raw_requestline)
        print(self.headers)

        address = self.path.split(':', 1)
        address[1] = int(address[1]) or 443

        try:
            s = socket.create_connection(proxy_address, timeout=self.timeout)
        except:
            self.send_error(502)
            return

        request = "GET / HTTP/1.1\r\n"
        request += f"Host: {proxy_address}\r\n"
        request += "User-Agent: Custom User-Agent\r\n"
        request += "Accept-Language: en-US,en;q=0.9\r\n"
        request += f"secret-connect: {str(address)}\r\n"
        request += "Connection: close\r\n"
        request += "\r\n"

        s.sendall(request.encode())

        self.send_response(200, 'Connection Established')
        self.end_headers()


class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    pass

print("running local server on 127.0.0.1:80")
httpd = ThreadedHTTPServer(("127.0.0.1", 80), MyRequestHandler)
httpd.serve_forever()
