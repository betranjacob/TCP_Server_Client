# Import socket module
import socket
from _thread import start_new_thread
import time

SERVER_RESPONSE_SIZE=25


def timing(f):
    """
    A utility function to meaure the time consumed
    in a function.

    :param: function to be profiled
    :return:
    """
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('%s function took %0.3f seconds' % (f.__name__, (time2-time1)))
        return ret
    return wrap


def client_send_thread(s, requests):
    """
     This thread make requests to server.

    :param s: Socket
    :param requests: NUmber of requests
    :return:
    """
    for i in range(0, int(requests)):
        # Create client message
        prefix = "137.72.95." + str(i).zfill(3)
        message_foo = prefix + ":foo"
        message_bar = prefix + ":bar"

        # message sent to server
        s.send(message_foo.encode('ascii'))
        s.send(message_bar.encode('ascii'))


@timing
def Main():

    # local host IP '127.0.0.1'
    host = '127.0.0.1'

    # Response integer values initialised to zero
    # This is icremented/decremented based on the responses received.
    foo_response_count = 0
    bar_response_count = 0

    # Total number of responses expected from server.
    total_expected_responses = 512

    # Define the port on which you want to connect
    port = 12346

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server on local computer
    s.connect((host, port))

    # Start a new thread to send requests to server.
    start_new_thread(client_send_thread, (s, total_expected_responses/2))

    while True:

        # message received from server
        s_data = s.recv(SERVER_RESPONSE_SIZE)
        data = str(s_data.decode('ascii'))
        #print(data)

        # Check if the response is positive or negative.
        negative = int(data.split(':')[3])

        if 'foo' in data:
            if negative:
                foo_response_count -= int(data.split(':')[2])
            else:
                foo_response_count += int(data.split(':')[2])

        elif 'bar' in data:
            if negative:
                bar_response_count -= int(data.split(':')[2])
            else:
                bar_response_count += int(data.split(':')[2])
        else:
            print('Spurious Data, Exiting - ', data)
            exit()

        # Decrement this value and exit the loop when it reaches 0.
        total_expected_responses -= 1
        if total_expected_responses == 0:
            break

    print('foo_response_count - ', foo_response_count)
    print('bar_response_count - ', bar_response_count)

    # close the connection
    s.close()


if __name__ == '__main__':
    Main()