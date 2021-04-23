import socket
import chatlib

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678


# HELPER SOCKET METHODS


def get_question(conn):
    code, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["get_question"], "")
    if code == chatlib.PROTOCOL_SERVER["error_msg"]:
        return code, str("ERROR get question")
    if code == chatlib.PROTOCOL_SERVER["no_questions_msg"]:
        return code, str("no more questions")
    return code, data


def get_question_answer_print(conn, question_id):
    answer = input("choice your answer: ")
    answer = chatlib.join_data([question_id, answer])
    code, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["send_answer"], answer)
    if code == chatlib.PROTOCOL_SERVER["error_msg"]:
        return str("ERROR get question")
    elif code == chatlib.PROTOCOL_SERVER["correct_answer_msg"]:
        return str("CORRECT ANSWER!!!")
    elif code == chatlib.PROTOCOL_SERVER["wrong_answer_msg"]:
        return str("WRONG ANSWER!!! :( \nThe correct answer is: " + data)


def print_question(question_data):
    question_toprint = "Q: " + question_data[1]
    for i in range(1, 5):
        question_toprint += "\n\t" + str(i) + ". " + question_data[i + 1]
    return question_toprint


def play_question(conn):
    # question[0] = id, question[1] = question_msg , question[2/3/4/5] = opt[1/2/3/4]
    cmd, data = get_question(conn)
    if cmd == chatlib.PROTOCOL_SERVER["question_msg"]:
        question_data = chatlib.split_data(data, 6)
        return question_data[0], print_question(question_data)
        # question[0] = id, question[1] = question_msg , question[n] = opt[n]
    return None, data


def get_score(conn):
    code, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["my_score"], "")
    if code == chatlib.PROTOCOL_SERVER["error_msg"]:
        return str("ERROR get score")
    return str("Your Score: " + data)


def get_highscore(conn):
    code, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["highscore"], "")
    if code == chatlib.PROTOCOL_SERVER["error_msg"]:
        return str("ERROR get highscore")
    return str("High-Score Table:\n" + data)


def get_logged_users(conn):
    code, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["logged_users"], "")
    if code == chatlib.PROTOCOL_SERVER["error_msg"]:
        return str("ERROR get logged users")
    return str("logged users:\n" + data)


def build_send_recv_parse(conn, code, data):
    build_and_send_message(conn, code, data)
    code, data = recv_message_and_parse(conn)
    return code, data


def build_and_send_message(conn, code, data):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Paramaters: conn (socket object), code (str), data (str)
    Returns: Nothing
    """
    protocol_msg = chatlib.build_message(code, data)
    # print('DEBUG_MSG: build_and_send_message(' + code + ', ' + data + ') return :' + protocol_msg)
    conn.send(protocol_msg.encode())


def recv_message_and_parse(conn):
    """
    Recieves a new message from given socket,
    then parses the message using chatlib.
    Paramaters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occured, will return None, None
    """
    full_msg = conn.recv(chatlib.MAX_MSG_LENGTH).decode()
    cmd, data = chatlib.parse_message(full_msg)
    return cmd, data


def connect():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((SERVER_IP, SERVER_PORT))
    return my_socket


def error_and_exit(error_msg):
    print(error_msg)
    exit(-2)


def register(conn, username, password):
    data = chatlib.join_data([username, password])
    cmd, server_msg = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["register_msg"], data)
    if cmd == chatlib.PROTOCOL_SERVER["register_ok_msg"]:
        return cmd
    return server_msg


def login(conn, username, password):
    data = chatlib.join_data([username, password])
    cmd, server_msg = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["login_msg"], data)
    if cmd == chatlib.PROTOCOL_SERVER["login_ok_msg"]:
        return cmd, False
    return server_msg, True


def logout(conn):
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")


def quit_cmd(conn):
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["exit_msg"], "")
    conn.close()
    exit(0)


def gui_print(msg):
    print(msg)


def main():
    conn = connect()
    menu = "########## MENU ##########\n" \
           "\t1.login\n" \
           "\t2.register\n" \
           "\t3.Quit\n"
    flag = True
    while flag:
        choice = input(menu + "Please enter your choice: ")
        if choice == '1':
            username = input("Please enter username: ")
            password = input("Please enter password: ")
            msg, flag = login(conn, username, password)
            gui_print(msg)
        elif choice == '2':
            username = input("Please enter username: ")
            password = input("Please enter password: ")
            gui_print(register(conn, username, password))
        elif choice == '3':
            quit_cmd(conn)

    menu = "########## MENU ##########\n" \
           "\t1.Play a trivia question\n" \
           "\t2.Get my score\n" \
           "\t3.Get high score\n" \
           "\t4.Get logged users\n" \
           "\t5.Quit\n"
    choice = input(menu + "Please enter your choice: ")
    while choice != '5':
        if choice == '1':
            question_id, data = play_question(conn)
            if question_id is not None:
                gui_print(data)
                gui_print(get_question_answer_print(conn, question_id))
            else:
                gui_print(data)
        elif choice == '2':
            gui_print(get_score(conn))
        elif choice == '3':
            gui_print(get_highscore(conn))
        elif choice == '4':
            gui_print(get_logged_users(conn))
        choice = input(menu + "Please enter your choice: ")
    logout(conn)
    gui_print("GoodBye")
    conn.close()


if __name__ == '__main__':
    main()
