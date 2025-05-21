# Client-Server Group Chat Application

This project is a Python-based client-server group chat application that allows multiple users to communicate in real time over a network. The system is implemented using Python sockets and threading, supporting group creation, joining, and secure messaging.

## Features
- **Multi-client support:** Multiple users can connect to the server and join group chats simultaneously.
- **Group management:**
  - Users can create new chat groups with a unique name and password.
  - Users can join existing groups by providing the correct group ID and password.
- **Secure access:** Group chats are protected by passwords to ensure only authorized users can join.
- **Real-time messaging:** Messages sent by any group member are instantly broadcast to all other members in the group.
- **Graceful disconnect:** Users can disconnect from the server at any time.

## Files
- `server.py`: The main server script. Handles client connections, group management, and message broadcasting.
- `client.py`: The client script. Allows users to connect to the server, join or create groups, and send/receive messages.
- `Server client groupchat.pdf`: Project documentation/report.

## Requirements
- Python 3.x
- No external libraries required (uses built-in `socket` and `threading` modules)

## Usage
### 1. Start the Server
On the host machine, run:
```bash
python server.py
```
The server will start listening for incoming client connections.

### 2. Start a Client
On each client machine, run:
```bash
python client.py
```

### 3. Client Options
Upon connecting, each client can:
- **Join an existing group chat** (option 1):
  - Enter your name, the group ID, and the group password.
- **Create a new group chat** (option 2):
  - Enter your name, choose a group password, and a new group will be created for you.
- **Exit** (option 3):
  - Disconnect from the server.

### 4. Messaging
- Once in a group, type your messages and press Enter to send.
- All group members will receive messages in real time.
- Type `qqq` to leave the chat.

## Example
```
$ python client.py
Hello client, please choose an option:
 1 - Connect to group chat
 2 - Create a group chat
 3 - Exit the server
1
Please enter your name:
Alice
Please enter the desired chat's ID:
1
Please enter the password for the desired chat:
password123
You have joined the chat with ID 1.
Alice: Hello everyone!
Bob has joined the chat!
Bob: Hi Alice!
```

## Notes
- The server and all clients must be on the same network or have appropriate firewall/port forwarding settings.
- The default server IP is `127.0.0.1` and port `7026` (client) / `7030` (server). Update these in the scripts if needed.

---

This project demonstrates the fundamentals of network programming, concurrency, and secure group communication in Python.
