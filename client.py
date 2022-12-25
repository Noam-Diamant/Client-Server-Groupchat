import socket
import time
import threading

# Import the necessary modules.

HOST_IP = '127.0.0.1'
PORT = 7023
ENCODING_METHOD = 'utf-8'
# Define constants for the server's host IP, port, and encoding method.

ADDRESS = (HOST_IP, PORT)


# Create a tuple for the server's address using the host IP and port.

def active_client():
    # This function handles the client's interaction with the server, including connecting to the
    # server, sending and receiving messages, and closing the connection.

    client_socket.connect((HOST_IP, PORT))  # Connect to the server's socket.

    opening_message = client_socket.recv(1024).decode(ENCODING_METHOD)
    print(opening_message)
    # Receive the opening message from the server in 1024-byte chunks and decode it using the ENCODING_METHOD.

    while True:
        # This loop prompts the user for an option based on the
        # opening message from the server and sends it to the server.
        # If the option is not valid, the loop repeats.

        option = input()
        # Prompt the user for an option based on the opening message from the server.

        client_socket.send(option.encode(ENCODING_METHOD))
        # Send the user's chosen option to the server.

        if option == '1' or option == '2' or option == '3':
            # If the option is valid, exit the loop.
            break
        else:
            # If the option is not valid, receive and print a message from the server and continue the loop.
            retry_message = client_socket.recv(1024).decode(ENCODING_METHOD)
            print(retry_message)
            continue

    if option == '3':
        # If the user has chosen option 3, disconnect from the server.
        disconnect_message = client_socket.recv(1024).decode(ENCODING_METHOD)
        print(disconnect_message)
        return
    # If the user has chosen option 1 or 2, continue with the connection.
    message_from_server = client_socket.recv(1024).decode(ENCODING_METHOD)
    print(message_from_server)
    if '1' in option:  # the first option, connect to a chat
        # If the user has chosen option 1, connect to an existing chat group.

        client_name = input()
        client_socket.send(client_name.encode(ENCODING_METHOD))
        message_from_server = client_socket.recv(1024).decode(ENCODING_METHOD)
        print(message_from_server)
        # Prompt the user for their name and send it to the server.
        # Receive and print a message from the server.

        while True:
            # This loop prompts the user for the group ID and sends it to the server until a valid group ID is provided.

            group_id = input()
            client_socket.send(group_id.encode(ENCODING_METHOD))
            message_from_server = client_socket.recv(1024).decode(ENCODING_METHOD)
            print(message_from_server)
            if 'invalid' not in message_from_server:
                # If the group ID is valid, exit the loop.
                break

        # Send and validate the password for the group.
        message_from_server = client_socket.recv(1024).decode(ENCODING_METHOD)
        print(message_from_server)
        confirmation_flag = False
        while not confirmation_flag:
            # This loop prompts the user for the password and sends it to the server
            # until a correct password is provided.
            password = input()
            client_socket.send(password.encode(ENCODING_METHOD))
            password_confirmation = client_socket.recv(1024).decode(ENCODING_METHOD)
            if "The password you provided for this group is correct" in password_confirmation:
                # If the password is correct, set the confirmation flag to True and exit the loop.
                print(password_confirmation)
                confirmation_flag = True
            else:
                print(password_confirmation)

    if '2' in option:
        # If the user has chosen option 2, create a new chat group.

        client_name = input()
        client_socket.send(client_name.encode(ENCODING_METHOD))
        # Prompt the user for their name and send it to the server.

        print(client_socket.recv(1024).decode(ENCODING_METHOD))
        # Receive and print a message from the server.

        password = input()
        client_socket.send(password.encode(ENCODING_METHOD))
        # Prompt the user for the password for the new chat group and send it to the server.

        print(client_socket.recv(1024).decode(ENCODING_METHOD))
        # Receive and print a message from the server.

    active_chat = threading.Thread(target=client_receive, args=(client_socket,))  # Creating new Thread object.
    # sender = threading.Thread(target=client_sen_massage, args=(client_socket, name))  # Creating new Thread object.
    active_chat.start()  # Starting the new thread (<=> handling new client)
    client_send(client_socket, client_name)

    # sender.start()  # Starting the new thread (<=> handling new client)

    client_socket.close()  # Closing client's connection with server (<=> closing socket)


def client_receive(client_socket):
    # This function listens for messages from the server and prints them to the console.
    # The client_socket parameter is not used in this function.

    while True:
        # This infinite loop continuously listens for messages from the server and prints them to the console.

        message = client_socket.recv(1024).decode(ENCODING_METHOD)
        # Receive a message from the server in 1024-byte chunks and decode it using the ENCODING_METHOD.

        if message == '###':
            # If the message is '###', it means the server has closed the connection,
            # so we exit the function.
            print('You have disconnected from the server, goodbye!')
            break

        print(message)
        # Print the message to the console.


def client_send(client_socket, name):
    # This function listens for input from the client and sends it to the server.
    # The client_socket and name parameters are not used in this function.

    while True:
        # This infinite loop continuously listens for input from the client and sends it to the server.

        send_msg = name + ': ' + input()
        # Concatenate the client's name and the input message, separated by a colon.

        client_socket.send(send_msg.encode(ENCODING_METHOD))
        # Encode the message using the ENCODING_METHOD and send it to the server.

        if 'qqq' in send_msg:
            # If the message contains 'qqq', it means the client has closed the connection,
            # so we exit the function.
            break


if __name__ == "__main__":
    # This block of code will only be executed if the script is run directly, not if it is imported
    # as a module.

    IP = socket.gethostbyname(socket.gethostname())
    # Get the host IP of the machine running the script.

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Create a new socket using the AF_INET address family (for IPv4) and the SOCK_STREAM socket type
    # (for a TCP connection).

    active_client()
    # Call the start_client function to connect to the server and start the chat.
