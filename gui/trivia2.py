#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 6.1
#  in conjunction with Tcl version 8.6
#    Apr 22, 2021 02:33:26 PM IDT  platform: Linux

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk

    py3 = False
except ImportError:
    import tkinter.ttk as ttk

    py3 = True

from gui import client_for_gui2 as trivia2_support, trivia


def vp_start_gui(conn):
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    top = Toplevel1(root, conn)
    trivia2_support.init(root, top)
    root.mainloop()


w = None


def create_Toplevel1(rt, *args, **kwargs):
    '''Starting point when module is imported by another module.
       Correct form of call: 'create_Toplevel1(root, *args, **kwargs)' .'''
    global w, w_win, root
    # rt = root
    root = rt
    w = tk.Toplevel(root)
    top = Toplevel1(w)
    trivia2_support.init(w, top, *args, **kwargs)
    return (w, top)


def destroy_Toplevel1():
    global w
    w.destroy()
    w = None


class Toplevel1:
    def __init__(self, top=None, conn=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'

        top.geometry("800x350+363+230")
        # top.minsize(1, 1)
        # top.maxsize(1345, 633)
        top.resizable(0, 0)
        top.title("Trivia Game")
        top.configure(highlightcolor="black")

        self.Labelframe1 = tk.LabelFrame(top)
        self.Labelframe1.place(relx=0.017, rely=0.0, relheight=0.957
                               , relwidth=0.190)
        self.Labelframe1.configure(relief='groove')
        self.Labelframe1.configure(text='''Menu''')

        self.play_button = tk.Button(self.Labelframe1)
        self.play_button.place(relx=0.071, rely=0.09, height=53, width=123
                               , bordermode='ignore')
        self.play_button.configure(borderwidth="2")
        self.play_button.configure(command=trivia2_support.play_question)
        self.play_button.configure(text='''Play Random''')

        self.get_score_button = tk.Button(self.Labelframe1)
        self.get_score_button.place(relx=0.071, rely=0.269, height=53, width=123
                                    , bordermode='ignore')
        self.get_score_button.configure(borderwidth="2")
        self.get_score_button.configure(command=trivia2_support.get_score)
        self.get_score_button.configure(text='''My Score''')

        self.get_highscore_button = tk.Button(self.Labelframe1)
        self.get_highscore_button.place(relx=0.071, rely=0.448, height=53
                                        , width=123, bordermode='ignore')
        self.get_highscore_button.configure(activebackground="#f9f9f9")
        self.get_highscore_button.configure(borderwidth="2")
        self.get_highscore_button.configure(command=trivia2_support.get_highscore)
        self.get_highscore_button.configure(text='''Top Players''')

        self.logged_button = tk.Button(self.Labelframe1)
        self.logged_button.place(relx=0.071, rely=0.627, height=53, width=123
                                 , bordermode='ignore')
        self.logged_button.configure(activebackground="#f9f9f9")
        self.logged_button.configure(borderwidth="2")
        self.logged_button.configure(command=trivia2_support.get_logged_users)
        self.logged_button.configure(text='''Logged Users''')

        self.quit_button = tk.Button(self.Labelframe1)
        self.quit_button.place(relx=0.071, rely=0.806, height=53, width=123
                               , bordermode='ignore')
        self.quit_button.configure(activebackground="#f9f9f9")
        self.quit_button.configure(borderwidth="2")
        self.quit_button.configure(command=trivia2_support.logout)
        self.quit_button.configure(text='''Logout''')

        self.Labelframe2 = tk.LabelFrame(top)
        self.Labelframe2.place(relx=0.22, rely=0.543, relheight=0.414
                               , relwidth=0.76)
        self.Labelframe2.configure(relief='groove')

        self.opt1_button = tk.Button(self.Labelframe2)
        self.opt1_button.place(relx=0.018, rely=0.138, height=53, width=280
                               , bordermode='ignore')
        self.opt1_button.configure(activebackground="#f9f9f9")
        self.opt1_button.configure(borderwidth="2")
        self.opt1_button.configure(command=trivia2_support.opt1)
        self.opt1_button.configure(wraplength=250)

        self.opt2_button = tk.Button(self.Labelframe2)
        self.opt2_button.place(relx=0.018, rely=0.552, height=53, width=280
                               , bordermode='ignore')
        self.opt2_button.configure(activebackground="#f9f9f9")
        self.opt2_button.configure(borderwidth="2")
        self.opt2_button.configure(command=trivia2_support.opt2)
        self.opt2_button.configure(wraplength=250)

        self.opt3_button = tk.Button(self.Labelframe2)
        self.opt3_button.place(relx=0.505, rely=0.138, height=53, width=280
                               , bordermode='ignore')
        self.opt3_button.configure(activebackground="#f9f9f9")
        self.opt3_button.configure(borderwidth="2")
        self.opt3_button.configure(command=trivia2_support.opt3)
        self.opt3_button.configure(wraplength=250)

        self.opt4_button = tk.Button(self.Labelframe2)
        self.opt4_button.place(relx=0.505, rely=0.552, height=53, width=280
                               , bordermode='ignore')
        self.opt4_button.configure(activebackground="#f9f9f9")
        self.opt4_button.configure(borderwidth="2")
        self.opt4_button.configure(command=trivia2_support.opt4)
        self.opt4_button.configure(wraplength=250)

        self.Frame1 = tk.Frame(top)
        self.Frame1.place(relx=0.22, rely=0.024, relheight=0.5, relwidth=0.76)
        self.Frame1.configure(relief='groove')
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief="groove")

        self.server_msg = tk.Label(self.Frame1)
        self.server_msg.place(relx=0.022, rely=0.057, height=151, width=560)
        self.server_msg.configure(wraplength=400)

        self.conn = conn


if __name__ == '__main__':
    trivia.vp_start_gui()
