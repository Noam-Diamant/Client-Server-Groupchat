import socket
import threading
import time

# Import the necessary modules.

HOST_IP = '127.0.0.1'
PORT = 7030
ENCODING_METHOD = 'utf-8'
# Define constants for the server's host IP, port, and encoding method.

ADDRESS = (HOST_IP, PORT)
# Create a tuple for the server's address using the host IP and port.

id_counter = 0
# Initialize a counter for generating unique IDs for clients.

active_connections = []
# Create a list to store the active connections.

groups = {}
# Create a dictionary to store the groups and their members.

sent_massage = ''
# Create a variable to store the message sent by a client.


def activate_server():
    # This function starts the server and listens for incoming connections.

    server_socket.bind(ADDRESS)
    # Bind the server socket to the specified IP+PORT tuple specified in the ADDRESS variable.

    print(f"The server is listening on address {ADDRESS} for connections...")
    # Print a message indicating the server is listening for connections.

    server_socket.listen()
    # Start listening for incoming connections.

    while True:
        # This infinite loop continuously listens for and accepts new connections.

        client_connection, address = server_socket.accept()
        # Accept a new connection and retrieve the connection and address of the client.

        print(f"New connection from {address}")
        # Print a message indicating a new connection has been established.

        client_thread = threading.Thread(target=handle_client, args=(client_connection, address))
        # Create a new thread to handle the client connection. The handle_client function is
        # specified as the target, and the connection and address variables are passed as arguments.

        client_thread.start()
        # Start the thread to handle the client connection.


def handle_client(client_socket, address):
    # This function handles a client connection. It receives the connection and address of the client
    # as arguments.

    try:
        # global variables for the ID count and groups dictionary
        global id_counter
        global groups

        # send main menu options to the client
        client_socket.send(
            "Hello client, please choose an option:\n 1 - Connect to group chat\n 2 - Create a group chat\n"
            " 3 - Exit the server\n".encode(ENCODING_METHOD))

        while True:
            # This loop receives the option selected by the client
            # from the main menu and verifies that it is a valid option.

            # receive the option selected by the client
            option = client_socket.recv(1024).decode(ENCODING_METHOD)
            if option == '1' or option == '2' or option == '3':
                # If the option is valid, print a message and exit the loop.
                print(f"client from address {address} chose option {option} from the main menu.\n")
                break
            else:
                # If the option is not valid, print a message and return the client to the main menu.
                print(
                    f"client from address {address} chose an invalid option {option}. returning him to the main menu.\n")
                client_socket.send("You chose an invalid choice, try again!".encode(ENCODING_METHOD))
                continue

        # if the client selects option 3, disconnect them from the server
        if option == '3':
            print(f"client on address {address} has disconnected. ")
            client_socket.send("You have disconnected from the server. Bye!".encode(ENCODING_METHOD))
            return

        # if the client selects option 1, request their name and desired group ID and password
        if '1' in option:
            # If a client wants to connect to a chat
            # but no chats are available, disconnect the client
            if not groups:
                client_socket.send("You have chosen to connect to a chat, but there are no chats available to connect "
                                   "to. You are disconnected from the server, you can try to connect again later, "
                                   "bye!".encode(ENCODING_METHOD))
                print(f"client on address {address} has disconnected, because there are no chats available to connect.\n")
                return

            # If chats are available, continue with the client connection process
            client_socket.send("Please enter your name: ".encode(ENCODING_METHOD))
            name = client_socket.recv(1024).decode(ENCODING_METHOD)

            client_socket.send("Please Enter the desired chat's ID: ".encode(ENCODING_METHOD))
            # loop until a valid group ID is received
            while True:
                group_id = client_socket.recv(1024).decode(ENCODING_METHOD)
                # if the group ID is not in the groups dictionary, send an error message and request the ID again
                if group_id not in groups.keys():
                    client_socket.send("The ID you provided is invalid, please try again! ".encode(ENCODING_METHOD))
                # if the group ID is valid, exit the loop
                else:
                    client_socket.send("The ID you provided is valid.".encode(ENCODING_METHOD))
                    print(f'Got a valid group ID, {group_id}, from client from {address}, {name}.')
                    break
            # request the password for the group
            client_socket.send("Please Enter the password for the desired chat: ".encode(ENCODING_METHOD))
            # loop until a valid password is received
            while True:
                password = client_socket.recv(1024).decode(ENCODING_METHOD)
                # if the password is correct, add the connection to the group's
                # connections list and send a confirmation message
                if groups[group_id]['password'] == password:
                    groups[group_id]['connections'].append(client_socket)
                    client_socket.send(f'The password you provided for this group is correct,\nyou are now connected to '
                                    f'group chat {group_id}.\nEvery message you send will be sent to every member of '
                                    f'the group.'.encode(ENCODING_METHOD))
                    print(
                        f"Got valid password for chat with ID {group_id}, from client from address {address}, {name}.")
                    print(f"client from address {address}, {name}, has joined the chat with ID {group_id}.\n")
                    # send a notify message to all clients in the chat
                    # about the new entrant
                    broadcast(client_socket, ['notify message', f'{name}'], group_id)
                    break
                # if the password is incorrect, send an error message and request the password again
                else:
                    client_socket.send('The password you provided is invalid, please try again! '.encode(ENCODING_METHOD))
        elif '2' in option:
            # If the client has chosen option 2, create a new chat group.

            client_socket.send("Please enter your name: ".encode(ENCODING_METHOD))
            # Send a message to the client asking for their name.

            name = client_socket.recv(1024).decode(ENCODING_METHOD)
            # Receive the client's name and decode it using the ENCODING_METHOD.

            client_socket.send("Please Enter the password for your group:".encode(ENCODING_METHOD))
            # Send a message to the client asking for a password for their group.

            password = client_socket.recv(1024).decode(ENCODING_METHOD)
            # Receive the password for the group and decode it using the ENCODING_METHOD.

            groups[str(id_counter)] = {'connections': [client_socket], 'password': password,
                                     'threads': []}
            # Create a new entry in the groups dictionary for the new group. The group's ID is the
            # current value of the id_count variable, and the group's connections and password are
            # specified by the connection and password variables, respectively. The threads list is
            # initially empty.

            group_id = str(id_counter)
            # Store the group's ID in the group_id variable.

            id_counter += 1
            # Increment the id_count variable.

            print(f'client from address {address}, {name}, has created chat with ID {group_id}.')
            # Print a message indicating that the client has created a new chat group.

            client_socket.send(
                f"You have successfully created a chat.\nthe chat's ID is {group_id}.".encode(ENCODING_METHOD))
            # Send a message to the client indicating that the chat group has been created successfully
            # and specifying the group's ID.

    except Exception as e:
        # If an exception occurs, print a message indicating that the client connection has been interrupted
        # and the address of the client. Then, print the error message.
        print("[CLIENT CONNECTION INTERRUPTED] on address: ", address)
        print(e)

    active_chat = threading.Thread(target=broadcast, args=(client_socket, name, group_id))
    # Create a new thread to run the broadcast function. The connection, name, and group_id
    # variables are passed as arguments.

    groups[group_id]['threads'].append(active_chat)
    # Append the receiver thread to the
    # list of threads for the group specified by the group_id variable.

    active_chat.start()
    # Start the receiver thread.


def broadcast(sender, name, group_to_send):
    # This function sends messages from the sender to all other members of the group
    # specified by the group_to_send parameter. The sender and name parameters are not
    # used in this function.

    try:
        # This block of code is inside a try-except block to catch any exceptions that may occur
        # while sending the messages.

        # notify message in case of a new client client
        # joining a chat
        if name[0] == 'notify message':
            for member in groups[group_to_send]['connections']:
                # Iterate through all the members of the group.
                if member != sender:
                    # If the member is not the sender, send the notify message to them.
                    member.send(f'{name[1]} has joined the chat!'.encode(ENCODING_METHOD))
                    # Encode the message using the ENCODING_METHOD and send it to the member.
            return

        while True:
            # This infinite loop continuously receives messages from the sender and sends them
            # to all other members of the group.

            message_to_send = sender.recv(1024).decode(ENCODING_METHOD)
            # Receive a message from the sender and decode it using the ENCODING_METHOD.
            # The message is received in 1024-byte chunks.

            if message_to_send == 'qqq':
                # If the message is 'qqq', it means the sender has closed the connection,
                # so we exit the function.
                print(f'{name} has left the chat server!')
                return

            for member in groups[group_to_send]['connections']:
                # Iterate through all the members of the group.
                if member != sender:
                    # If the member is not the sender, send the message to them.
                    member.send(message_to_send.encode(ENCODING_METHOD))
                    # Encode the message using the ENCODING_METHOD and send it to the member.
    except Exception as e:
        # If an exception occurs, print the error message.
        print(e)


# main function
if __name__ == '__main__':
    # This block of code will only be executed if the script is run directly, not if it is imported
    # as a module.

    IP = socket.gethostbyname(socket.gethostname())
    # Get the host IP of the machine running the script.

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Create a new socket using the AF_INET address family (for IPv4) and the SOCK_STREAM socket type
    # (for a TCP connection).

    activate_server()
    # Call the start_server function to start the server and listen for incoming connections.

    print("THE END!")
    # Print a message indicating the end of the script.
