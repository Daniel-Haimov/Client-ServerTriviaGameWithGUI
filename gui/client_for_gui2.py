import chatlib

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

# GLOBALS
root = None
top = None
args = []
kwargs = []
opt_buttons = []

question_data = [-1]


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
    try:
        protocol_msg = chatlib.build_message(code, data)
        top.conn.send(protocol_msg.encode())
    except ConnectionResetError:
        from gui import trivia
        trivia.vp_start_gui()


def recv_message_and_parse():
    """
    Recieves a new message from given socket,
    then parses the message using chatlib.
    Paramaters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occured, will return None, None
    """
    try:
        full_msg = top.conn.recv(chatlib.MAX_MSG_LENGTH).decode()
        cmd, data = chatlib.parse_message(full_msg)
        return cmd, data
    except ConnectionAbortedError:
        from gui import trivia
        trivia.vp_start_gui()


# Handle

def send_question_answer_get_result(answer, question_id):
    global question_data
    answer = chatlib.join_data([question_id, answer])
    code, data = build_send_recv_parse(chatlib.PROTOCOL_CLIENT["send_answer"], answer)
    return code, data


def get_question():
    code, data = build_send_recv_parse(chatlib.PROTOCOL_CLIENT["get_question"], "")
    if code == chatlib.PROTOCOL_SERVER["error_msg"]:
        return code, "ERROR get question"
    if code == chatlib.PROTOCOL_SERVER["no_questions_msg"]:
        return code, "no more questions"
    return code, data


def play_question():
    flush_console()
    global question_data
    # question_data[0] = question_id, question_data[1] = question_msg , question_data[2/3/4/5] = opt[1/2/3/4]
    cmd, data = get_question()
    if cmd == chatlib.PROTOCOL_SERVER["question_msg"]:
        try:
            question_data = chatlib.split_data(data, 6)
            top.server_msg.configure(text=question_data[1])
            for i in range(len(opt_buttons)):  # 0 < i < 3
                opt_buttons[i].configure(text=question_data[i + 2])
        except TypeError:
            question_data = [-1]
            top.server_msg.configure(text="ERROR get question, try again")
    else:
        top.server_msg.configure(text=data)


def get_score():
    flush_console()
    code, data = build_send_recv_parse(chatlib.PROTOCOL_CLIENT["my_score"], "")
    if code == chatlib.PROTOCOL_SERVER["error_msg"]:
        top.server_msg.configure(text="ERROR get score")
    top.server_msg.configure(text=str("Your Score: " + data))


def get_highscore():
    flush_console()
    code, data = build_send_recv_parse(chatlib.PROTOCOL_CLIENT["highscore"], "")
    if code == chatlib.PROTOCOL_SERVER["error_msg"]:
        top.server_msg.configure(text="ERROR get highscore")
    top.server_msg.configure(text=str("High-Score Table:\n" + data))


def get_logged_users():
    flush_console()
    code, data = build_send_recv_parse(chatlib.PROTOCOL_CLIENT["logged_users"], "")
    if code == chatlib.PROTOCOL_SERVER["error_msg"]:
        top.server_msg.configure(text="ERROR get logged users")
    top.server_msg.configure(text=str("logged users:\n" + data))


def init(root_init, top_init, *args_init, **kwargs_init):
    global root, top, args, kwargs, opt_buttons
    root = root_init
    top = top_init
    args = args_init
    kwargs = kwargs_init
    opt_buttons = [top.opt1_button, top.opt2_button, top.opt3_button, top.opt4_button]


def flush_console():
    global question_data
    grey = "#f9f9f9"
    question_data = [-1]
    top.server_msg.configure(text="")
    for button in opt_buttons:
        button.configure(text="")
        button.configure(background=grey)


def handle_opt(opt: int):
    global question_data
    question_id = question_data[0]
    green, red = "#00ff00", "#ff0000"
    if question_id == -1:
        return
    code, data = send_question_answer_get_result(opt, question_id)
    if code == chatlib.PROTOCOL_SERVER["error_msg"]:
        top.server_msg.configure(text="ERROR get question")
    elif code == chatlib.PROTOCOL_SERVER["correct_answer_msg"]:
        top.server_msg.configure(text=question_data[1] + '\n' + "CORRECT ANSWER!!!")
        opt_buttons[opt - 1].configure(background=green)
    elif code == chatlib.PROTOCOL_SERVER["wrong_answer_msg"]:
        top.server_msg.configure(
            text=str(question_data[1] + '\n' + "WRONG ANSWER!!! :( \nThe correct answer is: " + question_data[
                int(data) + 1]))
        opt_buttons[int(data) - 1].configure(background=green)
        opt_buttons[opt - 1].configure(background=red)
    question_data[0] = -1


def opt1():
    handle_opt(1)


def opt2():
    handle_opt(2)


def opt3():
    handle_opt(3)


def opt4():
    handle_opt(4)


def logout():
    build_and_send_message(chatlib.PROTOCOL_CLIENT["exit_msg"], "")
    top.conn.close()
    exit(0)


if __name__ == '__main__':
    from gui import trivia

    trivia.vp_start_gui()
