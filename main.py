import socket
import ssl


def forward_to_server(request, target_host, target_port, client_socket):
    # Create a socket and connect to the target server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as target_socket:
        target_socket.connect((target_host, int(target_port)))

        # Send the request to the target serve
        print("Sent: " + str(request))

        if str(request).startswith("b'CONNECT"):
            print("SSL")
            ssl_target = get_ssl_socket(target_socket, target_host, target_port)

            # Send a successful response to the client
            client_socket.send(b"HTTP/1.1 200 OK\r\n\r\n")
            ssl_connection(ssl_target, client_socket)
        else:
            target_socket.send(request)



def ssl_connection(target_socket, client_socket):
    while True:
        try:
            request = client_socket.recv(8192)
        except:
            break
        print("SSL-Request: " + str(request))
        if not request:
            break
        response = target_socket.send(request)
        print("SSL-Response: " + str(response))
        client_socket.send(bytes(response))

    target_socket.close()
    client_socket.close()


def server_proxy(proxy_host, proxy_port):
    # Create a socket and bind it to the proxy host and port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_socket:
        proxy_socket.bind((proxy_host, proxy_port))
        proxy_socket.listen(5)

        print(f"[*] Listening on {proxy_host}:{proxy_port}")

        while True:
            # Accept a client connection
            client_socket, address = proxy_socket.accept()

            print(f"[*] Accepted connection from {address[0]}:{address[1]}")

            request = client_socket.recv(8192)
            print("Request: " + str(request))

            if str(request).startswith("b'CONNECT"):
                str_request = str(request)
                target_url = str_request[0:str(request).find("H")]
                target_url = target_url[9:]
                target_url = target_url.replace(" ", "")

                target_host, target_port = target_url.split(":")

                # Forward the CONNECT request to the target server
                forward_to_server(request, target_host, target_port, client_socket)

            else:
                # Handle regular HTTP request forwarding
                target_host, target_port = get_host_and_port(request)

                response = forward_to_server(request, target_host, int(target_port))

                if response is not None:
                    client_socket.send(response)

            # Close the client socket
            client_socket.close()


def get_ssl_socket(socket, target_host, target_port):
    # Wrap the socket with SSL/TLS
    ssl_context = ssl.create_default_context()
    ssl_socket = ssl_context.wrap_socket(socket, server_hostname=target_host)

    return ssl_socket


def get_host_and_port(request):
    # Extract the target host and port from the request
    request_str = request.decode('utf-8')
    host_start = request_str.find('Host: ') + 6
    host_end = request_str.find('\r\n', host_start)
    host = request_str[host_start:host_end]

    if ':' in host:
        host, port = host.split(':')
    else:
        port = 80

    return host, port


server_proxy("127.0.0.1", 8882)
