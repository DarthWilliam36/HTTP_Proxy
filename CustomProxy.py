import socket
import select


class CustomProxy:
    def connect_relay(self, target_connection):

        conns = [self.connection, target_connection]
        self.timeout = 30 * 60
        self.connection.settimeout(3)
        target_connection.settimeout(3)

        def close_connections():
            for conn in conns:
                conn.close()

        print("New Connection: " + str(self.connection.getpeername()))

        while True:
            rlist, wlist, xlist = select.select(conns, [], conns, self.timeout)
            if xlist or not rlist:
                print("Connection timeout")
                close_connections()
                return

            for r in rlist:
                other = conns[1] if r is conns[0] else conns[0]
                data = r.recv(65535)
                if not data:
                    print("Broke Connection: " + str(self.connection.getpeername()))
                    close_connections()
                    return

                other.sendall(data)

    def try_connect(self, address):
        try:
            s = socket.create_connection(address, timeout=self.timeout)
            return s
        except:
            self.send_error(502)
            return False