import socket
import select


class CustomProxy:
    def connect_relay(self, target_connection):

        conns = [self.connection, target_connection]
        self.close_connection = False
        self.timeout = 5
        self.connection.settimeout(2)
        target_connection.settimeout(2)

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

    def try_connect(self, address):
        try:
            s = socket.create_connection(address, timeout=self.timeout)
            return s
        except:
            self.send_error(502)
            return False