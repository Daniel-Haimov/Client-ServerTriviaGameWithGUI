# Protocol Constants

CMD_FIELD_LENGTH = 16  # Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4  # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10 ** LENGTH_FIELD_LENGTH - 1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages 
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {"login_msg": "LOGIN", "logout_msg": "LOGOUT", "logged_users": "LOGGED",
                   "get_question": "GET_QUESTION", "send_answer": "SEND_ANSWER", "my_score": "MY_SCORE",
                   "highscore": "HIGHSCORE", "register_msg": "REGISTER", "exit_msg": "EXIT"}
# .. Add more commands if needed
PROTOCOL_SERVER = {"login_ok_msg": "LOGIN_OK", "login_failed_msg": "LOGIN_FAILED", "logged_msg": "LOGGED_ANSWER",
                   "question_msg": "YOUR_QUESTION", "correct_answer_msg": "CORRECT_ANSWER",
                   "wrong_answer_msg": "WRONG_ANSWER", "your_score_msg": "YOUR_SCORE", "all_score_msg": "ALL_SCORE",
                   "error_msg": "ERROR", "no_questions_msg": "NO_QUESTIONS",
                   "register_ok_msg": "REGISTER_OK", "register_failed_msg": "REGISTER_FAILED"}
# ..  Add more commands if needed


# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
    if len(cmd) > CMD_FIELD_LENGTH or len(data) > MAX_DATA_LENGTH:
        return ERROR_RETURN
    # if cmd not in PROTOCOL_CLIENT.values() or cmd not in PROTOCOL_SERVER.values():
    #     return ERROR_RETURN
    cmd = cmd + ' ' * (CMD_FIELD_LENGTH - len(cmd))
    data_str = str(len(data))
    while len(data_str) != 4:
        data_str = '0' + data_str
    full_msg = cmd + DELIMITER + data_str + DELIMITER + data
    return full_msg


def parse_message(data):
    tmp = str.split(data, DELIMITER)
    if len(tmp) != 3:
        return ERROR_RETURN, ERROR_RETURN
    if not tmp[1].replace(' ', '').isdecimal():
        return ERROR_RETURN, ERROR_RETURN
    cmd = tmp[0].replace(' ', '')
    msg = tmp[2]
    return cmd, msg


def split_data(msg, expected_fields):
    arr = str.split(msg, DATA_DELIMITER)
    if len(arr) == expected_fields:
        return arr
    return ERROR_RETURN


def join_data(msg_fields):
    data = ''
    for e in msg_fields:
        data += str(e) + DATA_DELIMITER
    data = data[0:-1]  # cut the last DATA_DELIMITER(#)
    return data
