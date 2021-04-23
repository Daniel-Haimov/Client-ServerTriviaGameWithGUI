##############################################################################
# server.py
##############################################################################

# IMPORTS
import socket
import chatlib
import select
import random
import ast
import html

# GLOBALS
client_sockets: list = list()
messages_to_send: list = list()
logged_users: dict = dict()

users: dict = dict()
file_users_directory = "data\\users.txt"

questions: dict = dict()
file_questions_directory = "data\\questions.txt"

SERVER_PORT = 5678
SERVER_IP = "0.0.0.0"

ERROR_MSG = "Error! "
CONNECTION_LOST = "CONNECTION_LOST!"
exit_msgs = [chatlib.PROTOCOL_CLIENT["logout_msg"], chatlib.PROTOCOL_CLIENT["exit_msg"], CONNECTION_LOST]


##############################################################################
# HELPER SOCKET METHODS
##############################################################################


def build_and_send_message(conn, code, msg):
    global messages_to_send
    full_msg = chatlib.build_message(code, msg)
    messages_to_send.append((conn, full_msg))


def recv_message_and_parse(conn):
    global exit_msgs, CONNECTION_LOST
    conn_peername = str(conn.getpeername())
    debug_print_msg = ''
    try:
        full_msg = conn.recv(chatlib.MAX_MSG_LENGTH).decode()
        debug_print_msg = "[" + conn_peername + "] SEND: " + full_msg
        if len(full_msg) == 0:
            return CONNECTION_LOST, conn_peername, debug_print_msg
        cmd, data = chatlib.parse_message(full_msg)
        if cmd in exit_msgs:
            data = conn_peername
        return cmd, data, debug_print_msg
    except ConnectionResetError:
        return CONNECTION_LOST, conn_peername, debug_print_msg


def setup_socket():
    """
    Creates new listening socket and returns it
    Recieves: -
    Returns: the socket object
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(0)
    return server_socket


def reset_globals():
    global client_sockets, logged_users, messages_to_send, users, questions
    client_sockets = list()
    messages_to_send = list()
    logged_users = dict()
    users = dict()
    questions = dict()


##############################################################################
# Data
##############################################################################

# QUESTIONS


def load_questions():
    global questions, file_questions_directory
    file_handler = open(file_questions_directory, 'rt')
    data = file_handler.read()
    if len(data) != 0:
        questions = dict(ast.literal_eval(data))
    file_handler.close()


# USERS


def get_user(username, password, score: int = 0, questions_asked: list=[]):
    user_data = dict()
    user_data["password"] = password
    user_data["score"] = score
    user_data["questions_asked"] = questions_asked
    return {username: user_data}


def add_user(username, password):
    global users
    user = get_user(username, password)
    users.update(user)


def update_users():
    global users, file_users_directory
    file = open(file_users_directory, 'wt')
    data = str(users)
    file.write(data)
    file.close()


def load_user_database():
    global users, file_users_directory
    file = open(file_users_directory, 'rt')
    data = file.read()
    if len(data) != 0:
        users = dict(ast.literal_eval(data))
    file.close()


def fix_data():
    global client_sockets, messages_to_send, logged_users, users, questions
    client_sockets = list(client_sockets)
    messages_to_send = list(messages_to_send)
    logged_users = dict(logged_users)
    users = dict(users)
    questions = dict(questions)


def restart_server(server_socket, exception_msg):
    print("\n\n\n--------Server fall--------")
    print(exception_msg)
    print("Saving...")
    fix_data()
    update_users()
    server_socket.close()
    reset_globals()
    print("Server try restarting")
    print("--------\n\n\n")
    main()
    print("Server failed restarting")


##############################################################################
# MESSAGE HANDLING HELPER
##############################################################################


def fix_html_code(s: str):
    tmp = html.unescape(s)
    tmp = tmp.replace("#", "")
    return tmp


def get_random_question(conn):
    global questions, logged_users, users
    username = logged_users.get(str(conn.getpeername()))
    user_history_question = (users.get(username))["questions_asked"]
    questions_array = list(questions.keys() - user_history_question)
    if len(questions_array) > 0:
        random_choice = random.choice(questions_array)
        question = questions[random_choice]
        answers = question.get('answers')
        question_str = fix_html_code(question.get('question'))
        for i in range(4):
            answers[i] = fix_html_code(answers[i])
        arr = [str(random_choice)] + [question_str] + answers
        return arr
    else:
        return ERROR_MSG


def sort_users_by_score():
    global users
    users = sorted(dict(users).items(), key=lambda x: x[1]["score"], reverse=True)


def send_error(conn, error_msg):
    """
    Send error message with given message
    Recieves: socket, message error string from called function
    Returns: None
    """
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["error_msg"], error_msg)


##############################################################################
# MESSAGE HANDLING
##############################################################################


def handle_register_message(conn, data):
    global users  # This is needed to access the same users dictionary from all functions
    user_info = chatlib.split_data(data, 2)
    if user_info is None:
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["error_msg"],
                               "Username and/or password cannot contain the # character")
    else:
        username = user_info[0]
        if username not in users:
            password = user_info[1]
            add_user(username, password)
            build_and_send_message(conn, chatlib.PROTOCOL_SERVER["register_ok_msg"], "")
        else:
            build_and_send_message(conn, chatlib.PROTOCOL_SERVER["error_msg"], "Username already exist")


def handle_login_message(conn, data):
    global users, logged_users
    user_info = chatlib.split_data(data, 2)
    if user_info is None:
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["error_msg"],
                               "Username and/or password cannot contain the # character")
    else:
        username = user_info[0]
        if username in users:
            password = user_info[1]
            right_password = (users.get(username)).get("password")
            if password == right_password:
                if username not in logged_users.values():
                    logged_users[str(conn.getpeername())] = username
                    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["login_ok_msg"], "")
                else:
                    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["error_msg"],
                                           "The user is already connected to the server")
            else:
                build_and_send_message(conn, chatlib.PROTOCOL_SERVER["error_msg"], "Wrong password!")
        else:
            build_and_send_message(conn, chatlib.PROTOCOL_SERVER["error_msg"], "Username does not exist")


def handle_logout_message(conn, data):
    global logged_users, client_sockets
    print(data, "Left")
    if data in logged_users:
        logged_users.pop(data)
    client_sockets.remove(conn)
    try:
        conn.close()
    except Exception as e:
        print(e)


def handle_question_message(conn):
    cmd = chatlib.PROTOCOL_SERVER["question_msg"]
    data = get_random_question(conn)
    if data != ERROR_MSG:
        build_and_send_message(conn, cmd, chatlib.join_data(data))
    else:
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["no_questions_msg"], "")


def handle_answer_message(conn, data):
    global questions, logged_users, users
    username = logged_users[str(conn.getpeername())]
    answer = chatlib.split_data(data, 2)
    question_id = int(answer[0])

    # need to add check if it his hacker(send protocol message) -- compare with user history questions...
    user_history_question = (users.get(username))["questions_asked"]
    if question_id in user_history_question:
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["error_msg"], "Hacker")
        # handle_logout_message(conn)
        # hacker
    else:
        ((users.get(username))["questions_asked"]).append(question_id)

    user_choice = answer[1]
    correct_answer = str((questions[question_id]).get("correct"))
    if user_choice == correct_answer:
        (users.get(username))["score"] = (users.get(username))["score"] + 5
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["correct_answer_msg"], "")
    else:
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["wrong_answer_msg"], correct_answer)


def handle_getscore_message(conn):
    global users
    username = logged_users.get(str(conn.getpeername()))
    score = str((users.get(username))['score'])
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["your_score_msg"], score)


def handle_highscore_message(conn):
    global users
    data = ''
    sort_users_by_score()
    for u in users:
        data += str("\t" + u[0] + ': ' + str(u[1]["score"]) + '\n')
    data = data[0:-1]
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["all_score_msg"], data)


def handle_logged_message(conn):
    global users, logged_users
    data = ''
    for u in logged_users:
        data += '\t' + logged_users[u] + '\n'
    data = data[0:-1]
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["logged_msg"], data)


################################


def handle_client_message(conn, cmd, data):
    """
    Gets message code and data and calls the right function to handle command
    Recieves: socket, message code and data
    Returns: None
    """
    global logged_users
    socket_perrname = str(conn.getpeername())
    fix_data()
    if socket_perrname in logged_users:
        if cmd == chatlib.PROTOCOL_CLIENT["get_question"]:
            return handle_question_message(conn)
        elif cmd == chatlib.PROTOCOL_CLIENT["send_answer"]:
            return handle_answer_message(conn, data)
        elif cmd == chatlib.PROTOCOL_CLIENT["logged_users"]:
            return handle_logged_message(conn)
        elif cmd == chatlib.PROTOCOL_CLIENT["my_score"]:
            return handle_getscore_message(conn)
        elif cmd == chatlib.PROTOCOL_CLIENT["highscore"]:
            return handle_highscore_message(conn)
    else:
        if cmd == chatlib.PROTOCOL_CLIENT["login_msg"]:
            return handle_login_message(conn, data)
        elif cmd == chatlib.PROTOCOL_CLIENT["register_msg"]:
            return handle_register_message(conn, data)
    return send_error(conn, "Unknown command")


def main():
    global users, logged_users, questions, messages_to_send, client_sockets, exit_msgs
    print("Welcome to Trivia Server!")
    print("Setting up server...")
    server_socket = setup_socket()
    load_questions()  # do from file...
    load_user_database()  # do from file...
    print("Listening for clients...")
    flag = True
    counter = 0
    try:
        while flag:
            ready_to_read, ready_to_write, in_error = \
                select.select([server_socket] + client_sockets, client_sockets, client_sockets)
            for current_socket in ready_to_read:
                if current_socket is server_socket:
                    (client_socket, client_address) = current_socket.accept()
                    print("New client joined!", client_address)
                    client_sockets.append(client_socket)
                else:
                    cmd, data, debug_print_msg = recv_message_and_parse(current_socket)
                    print(debug_print_msg)
                    if cmd in exit_msgs:
                        handle_logout_message(current_socket, data)
                        continue
                    handle_client_message(current_socket, cmd, data)
            for current_socket in ready_to_write:
                for message in messages_to_send:
                    (sendto_socket, msg_to_send) = message
                    if current_socket == sendto_socket:
                        print("[SERVER] " + msg_to_send)
                        current_socket.send(msg_to_send.encode())
                        messages_to_send.remove(message)
                        counter += 1
            if counter == 100:
                print("START Saving...")
                counter = 0
                update_users()
                print("Saving DONE...")
    except Exception as e:
        restart_server(server_socket, e)


if __name__ == '__main__':
    main()
