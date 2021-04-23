import ast
import random

questions = dict()
questions_from_web = dict()
fixed_questions_from_web = dict()
question_id = 0
file_questions_directory = "questions.txt"
file_questions_from_web_directory = 'question_from_web.txt'


def load_questions():
    global questions, file_questions_directory
    file_handler = open(file_questions_directory, 'rt')
    data = file_handler.read()
    if len(data) > 0:
        questions = dict(ast.literal_eval(data))
    file_handler.close()


def load_questions_from_web():
    global questions_from_web, file_questions_from_web_directory
    file_handler = open(file_questions_from_web_directory, 'rt')
    data = file_handler.read()
    if len(data) > 0:
        tmp_questions_from_web = dict(ast.literal_eval(data))
        questions_from_web = tmp_questions_from_web.get("results")
    file_handler.close()


def empty_file(path: str):
    file_handler = open(path, 'wt')
    file_handler.write("")
    file_handler.close()


def get_question(question, answers, correct):
    global question_id
    tmp = dict()
    tmp["question"] = question
    tmp["answers"] = answers
    tmp["correct"] = correct
    return {question_id: tmp}


def fix_question_str_0(question_str: str):
    question_str.replace("&#039;", "\'")
    question_str.replace("&quot;", "\"")
    question_str.replace("&amp;", "&")
    question_str.replace("&eacute;", "é")
    for i in range(0, 1000):
        if i < 10:
            question_str.replace("&#00" + str(i) + ";", "")
        elif i < 100:
            question_str.replace("&#0" + str(i) + ";", "")
        else:
            question_str.replace("&#" + str(i) + ";", "")
    question_str.replace("#", "")
    return question_str


def fix_html_str(s: str):
    return s
    # return str(html.unescape(s))


def fix_questions_from_web():
    global questions_from_web, fixed_questions_from_web, question_id
    for question in questions_from_web:
        question_str = fix_html_str(question.get("question"))
        correct_answer = fix_html_str(question.get("correct_answer"))
        incorrect_answers = question.get("incorrect_answers")
        for i in range(0, 2):
            incorrect_answers[i] = fix_html_str(incorrect_answers[i])
        answers = [correct_answer] + incorrect_answers
        random.shuffle(answers)
        correct = answers.index(correct_answer)
        fixed_questions_from_web.update(get_question(question_str, answers, correct + 1))
        question_id += 1


def save_questions(data: str):
    global questions, file_questions_directory
    file_handler = open(file_questions_directory, 'wt')
    try:
        file_handler.write(data)
    except UnicodeEncodeError as e:
        print(e)
        save_questions(str(questions))
    file_handler.close()


def add_questions():
    # just copy all from https://opentdb.com/api.php?amount=150&type=multiple
    # to file_questions_from_web_directory
    global questions, fixed_questions_from_web, question_id, file_questions_from_web_directory
    load_questions()
    question_id = len(questions)
    load_questions_from_web()
    empty_file(file_questions_from_web_directory)
    fix_questions_from_web()
    tmp = questions.copy()
    tmp.update(fixed_questions_from_web)
    save_questions(str(tmp))


if __name__ == '__main__':
    add_questions()
