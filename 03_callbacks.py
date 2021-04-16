import socket
import selectors
# module selectors has a higher level of abstraction in comparison to selector

# now we will create a default selector
selector = selectors.DefaultSelector()


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()

    # with the help of method .register() we will register sockets that are interesting to us
    # .register() is taking 3 objects: file object (with file number), interesting us event,
    # data that are connected with it (session id, function, etc.)
    selector.register(fileobj=server_socket, events=selectors.EVENT_READ, data=accept_connection)


def accept_connection(server_socket):
    client_socket, addr = server_socket.accept()
    print('Connection from', addr)

    # now we will register client's socket
    selector.register(fileobj=client_socket, events=selectors.EVENT_READ, data=send_message)


def send_message(client_socket):

    request = client_socket.recv(4096)

    if request:
        response = 'Hello world\n'.encode()
        client_socket.send(response)
    else:
        # also what is needed is before closing a socket we need to take it off the registration
        selector.unregister(client_socket)
        client_socket.close()


def event_loop():
    # here we will need to get a list of objects that are used for reading or for writing
    while True:

        # .select() will return a set of two objects, one is key
        # and the second one events (bite mask of reading/writing)
        events = selector.select()  # (key, events)

        for key, _ in events:
            callback = key.data
            callback(key.fileobj)


if __name__ == '__main__':
    server()
    event_loop()
