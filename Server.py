import socket
from _thread import start_new_thread
import threading
import time
from netaddr import IPAddress

CLIENT_REQUEST_SIZE=17
lock = threading.Lock()


def client_response_thread(c, wait, response):
    """
    Sleep for wait seconds and send response.
    :param c: socket
    :param wait: in seconds
    :param response: response string to send to client
    :return:
    """

    time.sleep(wait)
    lock.acquire()
    c.send(response.encode('ascii'))
    lock.release()

def client_request_thread(c, ip_cmd_map):
    """
     Thread fuction for every client

    :param c: Socket
    :return:
    """
    while True:

        # data received from client
        data = c.recv(CLIENT_REQUEST_SIZE)

        if not data:
            print('Client Exited...')
            break

        # send back string to client

        # Convert network order to byte order
        s_data = str(data.decode('ascii'))

        # Unpack IP and Command
        ip, cmd = s_data.split(':')

        # Convert the last octect to the format in file
        o_1, o_2, o_3, o_4 = ip.split('.')
        ip = o_1 + '.' + o_2 + '.' + o_3 + '.' + str(int(o_4))
        ip = str(IPAddress(ip))

        # Get response and wait time from Map.
        response = int(ip_cmd_map[ip][cmd][1])
        wait = int(ip_cmd_map[ip][cmd][0])

        # Set the Negative flag.
        negative = False
        if 0 > response:
            negative = True

        # Create the response data.
        s_data = s_data + ':' + str(abs(response)).zfill(5)
        if negative:
            s_data = s_data + ':' + str(1)
        else:
            s_data = s_data + ':' + str(0)

        #print('Sending - ', s_data)

        # Start a new thread to respond and continue loop with new requests
        start_new_thread(client_response_thread, (c, wait, s_data))

    # connection closed
    c.close()


def parse_data_file(filename):
    """

    :param filename:
    :return: A dictionary with delay and response mapped to ip_adress and cmd
    """

    ip_cmd_map={}
    with open(filename) as f:
        lines = open(filename).readlines()

        for l in lines:
            l = l.strip('\n')
            ip, cmd, response, delay = l.split(':')
            ip_cmd_map.setdefault(ip, {})
            ip_cmd_map[ip][cmd] = [delay, response]

    return ip_cmd_map


def Main():
    host = ""

    # Parse the input data file.
    ip_cmd_map = parse_data_file('data')

    port = 12346
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to post", port)

    # put the socket into listening mode
    # We have only one client, this can be any number.
    s.listen(1)
    print("socket is listening")

    # A forever loop until client wants to exit
    while True:
        # establish connection with client
        c, addr = s.accept()

        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(client_request_thread, (c, ip_cmd_map))

    s.close()


if __name__ == '__main__':
    Main()