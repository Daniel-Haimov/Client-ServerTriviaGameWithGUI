import socket
import chatlib

# GLOBALS
SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678

conn = None
root = None
top = None
args = []
kwargs = []


# HELPER SOCKET METHODS

def build_send_recv_parse(code, data):
    build_and_send_message(code, data)
    code, data = recv_message_and_parse()
    return code, data


def build_and_send_message(code, data):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Paramaters: conn (socket object), code (str), data (str)
    Returns: Nothing
    """
    global conn
    protocol_msg = chatlib.build_message(code, data)
    # print('DEBUG_MSG: build_and_send_message(' + code + ', ' + data + ') return :' + protocol_msg)
    conn.send(protocol_msg.encode())


def recv_message_and_parse():
    """
    Recieves a new message from given socket,
    then parses the message using chatlib.
    Paramaters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occured, will return None, None
    """
    global conn
    full_msg = conn.recv(chatlib.MAX_MSG_LENGTH).decode()
    cmd, data = chatlib.parse_message(full_msg)
    return cmd, data


def connect():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((SERVER_IP, SERVER_PORT))
    return my_socket


# Handle
def register():
    global conn, top
    username = top.usernameEntry.get()
    password = top.passwordEntry.get()
    if len(username) > 2 and len(password) > 2:
        data = chatlib.join_data([username, password])
        cmd, server_msg = build_send_recv_parse(chatlib.PROTOCOL_CLIENT["register_msg"], data)
        top.msgLabel.configure(text=server_msg)
        if cmd == chatlib.PROTOCOL_SERVER["register_ok_msg"]:
            top.msgLabel.configure(text=cmd)
    else:
        top.msgLabel.configure(text="Please enter a username and password of at least 3 characters each")


def login():
    global conn, top, root
    username = top.usernameEntry.get()
    password = top.passwordEntry.get()
    data = chatlib.join_data([username, password])
    cmd, server_msg = build_send_recv_parse(chatlib.PROTOCOL_CLIENT["login_msg"], data)
    top.msgLabel.configure(text=server_msg)
    if cmd == chatlib.PROTOCOL_SERVER["login_ok_msg"]:
        top.msgLabel.configure(text=cmd)
        root.destroy()
        from gui import trivia2
        trivia2.vp_start_gui(conn)


def quit_cmd():
    global conn
    build_and_send_message(chatlib.PROTOCOL_CLIENT["exit_msg"], "")
    conn.close()
    exit(0)


def init(root_init, top_init, *args_init, **kwargs_init):
    global conn, root, top, args, kwargs
    conn = connect()
    root = root_init
    top = top_init
    args = args_init
    kwargs = kwargs_init


if __name__ == '__main__':
    from gui import trivia

    trivia.vp_start_gui()
