import socket
import ssl
import threading


def handle_client(client_socket, target_host, target_port):
    # Connect to the target server
    target_address = (target_host, int(target_port))
    target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target_socket.connect(target_address)

    # Wrap target socket in SSL connection
    # ssl_context = ssl.create_default_context()
    # target_socket = ssl_context.wrap_socket(target_socket, server_hostname=target_host)

    # Send an HTTP 200 OK response to the client
    response = b"HTTP/1.1 200 OK\r\n\r\n"
    client_socket.sendall(response)

    # Forward data between the client and target server
    while True:
        # Receive data from the client
        client_data = client_socket.recv(65535)
        print("Client Data: " + str(client_data))

        if not client_data:
            break

        # Forward data to the target server
        target_socket.sendall(client_data)

        # Receive data from the target server
        target_data = target_socket.recv(65535)
        print("Target Data: " + str(target_data))

        if not target_data:
            break

        # Forward data to the client
        client_socket.sendall(target_data)

    # Close the sockets
    target_socket.close()
    client_socket.close()


def start_proxy():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_socket:
        proxy_socket.bind(("127.0.0.1", 8882))
        proxy_socket.listen(5)

        print("[*] Listening on")

        while True:
            # Accept a client connection
            client_socket, address = proxy_socket.accept()

            print(f"[*] Accepted connection from {address[0]}:{address[1]}")

            request = client_socket.recv(65535)
            print("Client Initial Request: " + str(request))

            if str(request).startswith("b'CONNECT"):
                # Handle CONNECT request separately
                str_request = str(request)
                target_url = str_request[0:str(request).find("H")]
                target_url = target_url[9:]
                target_url = target_url.replace(" ", "")

                target_host, target_port = target_url.split(":")

                # Create a new thread to handle the client connection
                client_thread = threading.Thread(target=handle_client, args=(client_socket, target_host, target_port))
                client_thread.start()
            else:
                # Handle regular HTTP request here
                host, port = get_host_and_port(request)
                target_address = (host, int(port))
                target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                target_socket.connect(target_address)

                target_socket.sendall(request)
                response = target_socket.recv(65535)
                client_socket.sendall(response)

                target_socket.close()


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

# Start the proxy server
start_proxy()

