import socket
from select import select
# here we will create two functions, server and client
# we have two tasks here:
# - which sockets are ready for reading and writing (we will use select here)
# - create a mechanism that will manage function execution (generator will be used)

# an algorithm which is used here was proposed by David Beazley
# 2015 PyCon
# Concurrency from the Ground up Live

# here we are creating a list that will be filled with generators
tasks = []

# here we create couple of dicts for saving sockets (key) and generators (values)
# for reading
to_read = {}

# for writing
to_write = {}


# as values our generators will send sockets
# we will send sockets to function .select() to filter which of them are ready

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()

    while True:
        # we are sending server_socket only after it turns being ready, what is said by .select()
        yield ('read', server_socket)
        client_socket, addr = server_socket.accept()  # here we are reading

        print("Connection from", addr)

        tasks.append(client(client_socket))


def client(client_socket):
    while True:
        # we will send tuples to understand which actions are we taking relative to sockets
        yield ('read', client_socket)
        request = client_socket.recv(4096)  # here we are reading

        if not request:
            break
        else:
            response = 'Hello world\n'.encode()

            yield ('write', client_socket)
            client_socket.send(response)  # here we are writing

    client_socket.close()


def event_loop():

    while any([tasks, to_read, to_write]):  # will return True if there will be anything in all values, otherwise False

        while not tasks:
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])  # list with errors will be empty

            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))
                # if we will pop dict, it will return value; key is deleted from dict
                # generator will be send to tasks, because it is value and socket is key

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))

        # now we will start generators and fill dicts with necessary pairs
        try:
            task = tasks.pop(0)  # task will hold tuple with 'read/write' and socket

            reason, sock = next(task)

            if reason == 'read':
                to_read[sock] = task
            if reason == 'write':
                to_write[sock] = task
        except StopIteration:
            print("Done!")


tasks.append(server())


