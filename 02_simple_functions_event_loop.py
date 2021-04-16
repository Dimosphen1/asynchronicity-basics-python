import socket
# to know which socket is now free and can process user's data, we will use select
from select import select

# select is a system function which is needed for monitoring of state changes of file objects from sockets
# .fileno() is a file descriptor / specific number of a file to which we can refer
# inside of .select() we will pass a list with variables, so we need to create them
to_monitor = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5000))
server_socket.listen()


# we will remove connection acceptation to the function
def accept_connection(server_socket):

    # we can delete while True cycle, because we created event loop
    client_socket, addr = server_socket.accept()
    print('Connection from', addr)

    # after that we need to monitor client's socket
    to_monitor.append(client_socket)

# sending and receiving user's massages we will also remove to the function
def send_message(client_socket):
# we delete while True cycle here because we also have event loop
    request = client_socket.recv(4096)

    if request:
        response = 'Hello world\n'.encode()
        client_socket.send(response)
    else:
        client_socket.close()


# now we will need to create a connection between several sockets for working with multiple clients
def event_loop():
    while True:
        # here we will track three lists: one with objects that will become available for reading
        # one for writing, one with objects where we wait for different mistakes
        # as the result select() will return the list of same objects but only when they will become available
        # _ means that there will be now variables for storing these values
        ready_to_read, _, _, = select(to_monitor, [], [])  # read, write, errors

        # after that we need to proceed the list "ready_to_read"
        for sock in ready_to_read:
            if sock is server_socket:
                accept_connection(sock)
            else:
                send_message(sock)



if __name__ == '__main__':
    to_monitor.append(server_socket)
    # after that we can start our event loop:
    event_loop()

    # accept_connection(server_socket)

# our goal to introduce asynchronicity is to remove connections with functions to make them independent
