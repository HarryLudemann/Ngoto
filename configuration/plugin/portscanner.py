from ngoto import Plugin
import socket, threading

class Plugin(Plugin):
    name = 'Port Scanner'
    version = 0.1
    description = 'Port Scanner'

    def TCP_connect(self, ip, port_number, delay, output):
        TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        TCPsock.settimeout(delay)
        try:
            TCPsock.connect((ip, port_number))
            output[port_number] = 'Listening'
        except:
            output[port_number] = ''

    def scan_ports(self, host_ip: str, delay: int, range_start: int, range_end: int):

        ports = []          
        threads = []        # To run TCP_connect concurrently
        output = {}         # For printing purposes

        # Spawning threads to scan ports
        for i in range(range_start, range_end):
            t = threading.Thread(target=self.TCP_connect, args=(host_ip, i, delay, output))
            threads.append(t)

        # Starting threads
        for i in range(range_start, range_end):
            threads[i-range_start].start()

        # Locking the main thread until all threads complete
        for i in range(range_start, range_end):
            threads[i-range_start].join()

        # Printing listening ports from small to large
        for i in range(range_start, range_end):
            if output[i] == 'Listening':
                ports.append(i)
        return ports

    def get_context(self, target: str, timeout: str, range_start: str, range_end: str):
        ports = self.scan_ports(target, int(timeout), int(range_start), int(range_end))
        context = {
            'ports': ports
        }
        return context

    def main(self, hz): # given CLT obj
        target = hz.interface.get_input("Enter host IP: ", '[Portscanner]', hz.curr_path)
        if target == 'back': return {}
        timeout = hz.interface.get_input("How many seconds the socket is going to wait until timeout: ", '[Portscanner]', hz.curr_path)
        if timeout == 'back': return {}
        start_range, end_range = hz.interface.get_input("Specify port range eg 50-100: ", '[Portscanner]', hz.curr_path).split('-')
        hz.interface.output("Please wait scanning ports...")
        return self.get_context(target, timeout, start_range, end_range)

    def print_info(self, hz, context, tables):
        col_widths = [20]
        col_names = ['Port']
        col_values = []
        for item in context['ports']:
            col_values.append( [str(item)] )

        hz.interface.output( '\n' + tables.get_table(col_names, col_widths, col_values) )

    def create_table(self):
        return '''
        CREATE TABLE IF NOT EXISTS email (
        id integer PRIMARY KEY AUTOINCREMENT,
        port text,
        '''
