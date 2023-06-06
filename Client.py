import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver

if os.path.isfile(os.path.join(os.getcwd(), 'CustomProxy.py')):
    from CustomProxy import CustomProxy
else:
    raise RuntimeError("CustomProxy.py not found in directory!")

proxy_address = ("", 80)
local_port = "80"
password = ""


class MyRequestHandler(BaseHTTPRequestHandler, CustomProxy):

    def do_CONNECT(self):
        print("Incoming CONNECT packet:")
        print(self.raw_requestline)
        print(self.headers)

        address = self.path.split(':', 1)
        address[1] = int(address[1]) or 443

        s = self.try_connect(proxy_address)
        if not s:
            return

        request = "GET / HTTP/1.1\r\n"
        headers = {
            'Host': proxy_address[0],
            'User-Agent': 'My Custom User Agent',
            'Accept': 'text/html',
            'secret-connect': f"{address[0]}:{address[1]}",
            "password": f"{password}"
        }

        for header, value in headers.items():
            request += f"{header}: {value}\r\n"
        request += "\r\n"

        s.sendall(request.encode())

        self.connect_relay(s)


class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    pass


print("running local server on 127.0.0.1:81")
httpd = ThreadedHTTPServer(("127.0.0.1", local_port), MyRequestHandler)
httpd.serve_forever()
