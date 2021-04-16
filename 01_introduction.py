import socket

# domain: 5000
# socket is a port which is used for interaction between two objects (client and server)

# here we will start with a server side
# AF_INET stands for Ipv4, SOCK_STREAM stands for TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# it is possible that there will be a delay during several client requests and port wouldn't be available
# this delay is needed for providing necessary time for client data transmission
# Now we will need to set options of our socket
# SOL_SOCKET is the socket layer itself. It is used for options that are protocol independent. 1 means True
# https://www.gnu.org/software/libc/manual/html_node/Socket_002dLevel-Options.html#Socket_002dLevel-Options
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# now we will say to what port and domain we will bind this socket
server_socket.bind(('localhost', 5000))

# now we need to set socket server to listening mode relative to buffer for receiving incoming connections
server_socket.listen()

# relation between server and client is undefined in time, so to keep it opened we will use endless cycle
while True:
    print("Before .accept()")
    # now we will describe client's socket
    # .accept() receives data from buffer
    # it has two elements in tuple: client's socket and address
    client_socket, addr = server_socket.accept()
    print('Connection from', addr)

    # after we created connection, we need to wait for some message from client
    while True:
        # print("Before .recv()")
        # we will specify what is the size of the message that we are going to receive, here it is 4 kilobytes
        request = client_socket.recv(4096)

        # conditions for interruption of this cycle
        if not request:
            break
        else:
            # here we will crate some response
            # we also need to transform this string to bytes
            response = "Hello word\n".encode()

            # after that we will send the response to the client_socket
            client_socket.send(response)


    print("Outside inner while loop")

    # at this level we also need to close client_socket
    client_socket.close()

# After that in a terminal we can run server with command python 01_introduction.py
# .accept() here is a blocking function or operation
# we can create an incoming connection with NetCut (nc), for that we write the following in terminal:
# nc localhost 5000

# after that we stopped on function client_socket.recv(4096) and will receive "Hello world" from server

# if we will connect another user, it will be impossible because server is working with first client
# inside the inner loop

# it will respond to the second client only when the first one is closed

# there is a problem on how to keep respond to the second user, while first thinks on what to send
# for that we need to go somehow outside of the inner while loop

# for that we need two ingredients:
# to send the control over program execution to somewhere (code manager) / event loop
# to write asynchronous code in 3 ways without the use of side libraries:
# callbacks, generators or syntax async / await



