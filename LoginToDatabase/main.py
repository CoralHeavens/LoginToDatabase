from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
import tkinter as tk
import os
import sqlite3 as sql
import sys
from itertools import cycle
from User import User

root = Tk()
Session = User('', '', True)
arithmetic_op = ['+', '-', '_', '=', '/', '*', '%', '^', '~']
nameDB = 'user_list'


class Table(tk.Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        super().__init__(parent)
        table = ttk.Treeview(self, show="headings", selectmode="browse")
        table["columns"] = headings
        table["displaycolumns"] = headings
        for head in headings:
            table.heading(head, text=head, anchor=tk.CENTER)
            table.column(head, anchor=tk.CENTER)
            for row in rows:
                table.insert('', tk.END, values=tuple(row))
                scrolltable = tk.Scrollbar(self, command=table.yview)
                table.configure(yscrollcommand=scrolltable.set)
                scrolltable.pack(side=RIGHT, fill=tk.Y)
                table.pack(expand=tk.YES, fill=tk.BOTH)


def Login_window():
    root.title("Coral Authorize")
    root.geometry(f"250x215+400+300")
    root['bg'] = '#add0d9'
    root.minsize(250, 215)
    root.maxsize(250, 215)

    blank_print()

    login_text = Label(root,
                       text="Login:",
                       width=20,
                       bg='#add0d9',
                       font=('impact', 13))
    login_entry = Entry(root,
                        font=('impact', 13),
                        width=20, )
    login_text.pack()
    login_entry.pack()

    password_text = Label(root,
                          text="Password:",
                          width=20,
                          bg='#add0d9',
                          font=('impact', 13))
    password_entry = Entry(root,
                           show='♦',
                           font=('impact', 13),
                           width=20)
    password_text.pack()
    password_entry.pack()

    blank_print()

    button_login = Button(root,
                          text="Log in",
                          width=20,
                          font=('impact', 13),
                          command=lambda: login_button(login_entry.get(), password_entry.get()))
    button_login.pack()

    info(root)

    root.mainloop()


def blank_print():
    blank = Label(text='',
                  bg='#add0d9')
    blank.pack()


def login_button(username, password):
    if try_user(username):
        if compare_pass(username, password):
            create_session(username)

        else:
            User.pass_try -= 1
            if User.pass_try == 0:
                sys.exit()
            messagebox.showwarning(title='Error', message='Password is incorrect.\n'
                                                          'You have ' + str(User.pass_try) + ' tries left.')
    else:
        messagebox.showwarning(title='Error', message='Unknown user.')


def Admin_panel():
    root.destroy()
    panelA = Tk()
    panelA.title(Session.get_username())
    panelA.geometry(f"250x375+600+300")
    panelA.minsize(250, 375)
    panelA.maxsize(250, 375)
    panelA['bg'] = '#add0d9'

    blank_print()

    reg_button = Button(panelA,
                        text="Register a new User",
                        width=20,
                        font=('impact', 13),
                        command=lambda: reg_panel())
    reg_button.pack()

    blank_print()

    change_button = Button(panelA,
                           text="Change password",
                           width=20,
                           font=('impact', 13),
                           command=lambda: change_password())
    change_button.pack()

    blank_print()

    ban_button = Button(panelA,
                        text="Ban hammer",
                        width=20,
                        font=('impact', 13),
                        command=lambda: ban())
    ban_button.pack()

    blank_print()

    view_button = Button(panelA,
                         text="View DataBase",
                         width=20,
                         font=('impact', 13),
                         command=lambda: view_db())
    view_button.pack()

    blank_print()

    wipe_button = Button(panelA,
                         text="Wipe DataBase",
                         width=20,
                         font=('impact', 13),
                         command=lambda: wipe_db())
    wipe_button.pack()

    blank_print()

    exit_button = Button(panelA,
                         text="Exit",
                         width=20,
                         font=('impact', 13),
                         command=lambda: exit())
    exit_button.pack()

    info(panelA)

    panelA.mainloop()


def info(panel):

    info_button = Button(panel,
                         text="?",
                         width=2,
                         height=1,
                         font=('impact', 12),
                         command=lambda: get_info())
    info_button.pack(side=LEFT)


def get_info():

    messagebox.showinfo(title='Info', message="""Ремха Богдан 125-18-2\n
    (c) CoralHeavens\n
    Вариант 14\n
    'Наявність малих і великих літер, а також знаків арифметичних операцій.'\n
    remkha.b.t@gmail.com""")


def User_panel():
    root.destroy()
    panelU = Tk()
    panelU.title(Session.get_username())
    panelU.geometry(f"250x150+600+300")
    panelU['bg'] = '#add0d9'
    panelU.minsize(250, 150)
    panelU.maxsize(250, 150)

    blank_print()

    change_button = Button(panelU,
                           text="Change password",
                           width=20,
                           font=('impact', 13),
                           command=lambda: change_password())
    change_button.pack()

    blank_print()

    exit_button = Button(panelU,
                         text="Exit",
                         width=20,
                         font=('impact', 13),
                         command=lambda: sys.exit())
    exit_button.pack()

    info(panelU)

    panelU.mainloop()


def reg(username, password, role, registration1):
    if password == '':

        insert_info(username, '', role)
        registration1.destroy()
        return

    elif check_pass(password=password):

        insert_info(username, password, role)
        registration1.destroy()
        return

    else:

        weak_window = Tk()
        weak_window.title('Error')
        weak_window.geometry(f"300x60+800+360")
        weak_window['bg'] = '#add0d9'

        messagebox.showwarning(title='Warning', message='Your password is too weak!')


def ban():
    ban_window = Tk()
    ban_window.title("Registration")
    ban_window.geometry(f"300x300+800+350")
    ban_window['bg'] = '#add0d9'

    blank_print()

    ban_label = Label(ban_window,
                      text="Enter username:",
                      width=20,
                      font=('impact', 16),
                      bg='#add0d9')
    ban_label.pack()

    blank_print()

    ban_enter = Entry(ban_window,
                      font=('impact', 13),
                      width=20)
    ban_enter.pack()

    blank_print()

    ban_butt = Button(ban_window,
                      text="BAN HAMMER",
                      width=20,
                      font=('impact', 13),
                      command=lambda: status_0(ban_enter.get(), ban_window))
    ban_butt.pack()


def status_0(name, window):
    con, cur = connect_base()
    cur.execute(f"""UPDATE user_list SET status = {False} WHERE username = '{name}'""")
    con.commit()
    cur.close()
    window.destroy()


def reg_panel():
    registration = Tk()
    registration.title("Registration")
    registration.geometry(f"300x300+800+350")
    registration['bg'] = '#add0d9'
    registration.minsize(300, 300)
    registration.maxsize(300, 300)

    blank_print()

    username_label = Label(registration,
                           text="Login:",
                           width=20,
                           font=('impact', 13),
                           bg='#add0d9')
    username_entry = Entry(registration,
                           font=('impact', 13),
                           width=20)
    username_label.pack()
    username_entry.pack()

    blank_print()

    password_label = Label(registration,
                           text="Password:",
                           width=20,
                           font=('impact', 13),
                           bg='#add0d9')
    password_entry = Entry(registration,
                           width=20,
                           font=('impact', 13),
                           show='♦')
    password_label.pack()
    password_entry.pack()

    blank_print()

    role_label = Label(registration,
                       text='Role:',
                       width=20,
                       font=('impact', 13),
                       bg='#add0d9')
    role_label.pack()

    combo_role = ttk.Combobox(registration,
                              state='readonly',
                              values=['User',
                                      'Admin'])
    combo_role['width'] = 20
    combo_role['font'] = ('impact', 13)
    combo_role.current(0)
    combo_role.pack()

    blank_print()

    reg_button = Button(registration,
                        width=20,
                        text='Register',
                        font=('impact', 13),
                        command=lambda: reg(username_entry.get(), password_entry.get(), combo_role.get(), registration))
    reg_button.pack()

    registration.mainloop()


def wipe_db():
    try:

        os.remove('user_list.db')
        createDB()
        messagebox.showwarning(title='New', message='Please, register an administrator.')
        reg_panel()

    except PermissionError:

        messagebox.showwarning(title='Error', message='Sorry, DataBase is opened in other program.'
                                                      '\nClose it before deleting.')


def view_db():
    con, cur = connect_base()
    cur.execute("""SELECT * FROM user_list""")
    content = (row for row in cur.fetchall())

    db_window = Tk()
    db_window.title("User List")
    db_table = Table(db_window, headings=('Username', 'Password', 'Role', 'Status'), rows=content)
    db_table.pack(expand=tk.YES, fill=tk.BOTH)

    db_window.mainloop()


def change_password():

    change = Tk()
    change.title('Change password for ' + str(Session.get_username()))
    change.geometry(f"200x250+750+300")
    change['bg'] = '#add0d9'
    change.minsize(200, 250)
    change.maxsize(200, 250)

    blank_print()
    blank_print()
    blank_print()

    old_pass_label = Label(change,
                           text="Old password:",
                           width=20,
                           font=('impact', 13),
                           bg='#add0d9')
    old_pass_entry = Entry(change,
                           show='♦',
                           font=('impact', 13),
                           width=20)
    old_pass_label.pack()
    old_pass_entry.pack()

    blank_print()

    new_pass_label = Label(change,
                           text="New password:",
                           width=20,
                           font=('impact', 13),
                           bg='#add0d9')
    new_pass_entry = Entry(change,
                           show='♦',
                           font=('impact', 13),
                           width=20)
    new_pass_label.pack()
    new_pass_entry.pack()

    blank_print()

    change_button = Button(change,
                           text='Confirm',
                           width=20,
                           font=('impact', 13),
                           command=lambda: confirm_change(str(old_pass_entry.get()), str(new_pass_entry.get()), change))
    change_button.pack(side=BOTTOM)


def confirm_change(old, new, win):

    name = Session.get_username()
    if compare_pass(name, old):
        con, cur = connect_base()
        new = (str(pass_cipher(new)))

        cur.execute("""UPDATE 'user_list' SET password = (?) WHERE username = (?)""", (new, name))

        con.commit()
        cur.close()
        win.destroy()

    else:
        messagebox.showwarning(title='Error', message='Password is incorrect.')
        return


def createDB():
    con, cur = connect_base()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS """
                + str(nameDB) +
                """ ('username' STRING, 'password' STRING, 'role' STRING, 'status' BOOLEAN)""")
    con.commit()
    cur.close()


def insert_info(username, password, role):
    password = pass_cipher(password=password)

    con, cur = connect_base()
    cur.execute("""INSERT INTO 'user_list' VALUES (?, ?, ?, ?);""", (str(username), str(password), str(role), True))
    con.commit()
    cur.close()


def check_pass(password):
    if check_upper(password) and check_lower(password) and check_operation(password):
        return True


def check_upper(password):
    for x in range(len(password)):
        if password[x].isupper():
            return True
    return False


def check_lower(password):
    for x in range(len(password)):
        if password[x].islower():
            return True
    return False


def check_operation(password):
    for x in range(len(password)):
        if password[x] in arithmetic_op:
            return True
    return False


def xor(message, key):
    return bytes(a ^ b for a, b in zip(message, cycle(key)))


def pass_cipher(password):
    key1 = b'this_is_key'
    key2 = b'also_here_another'
    result = xor(password.encode(), key1)

    return xor(result, key2)


def connect_base():
    con = sql.connect('user_list.db')
    cur = con.cursor()

    return con, cur


def compare_pass(username, password):
    check_password = extract_data('password', username)
    password = pass_cipher(password)

    return str(password) == str(check_password)


def create_session(username):
    role = extract_data('role', username)
    status = extract_data('status', username)

    if not status:
        messagebox.showwarning(title="Error", message="You've been blocked.\nContact Admin.")
        sys.exit()

    Session.set_all(username, role, status)
    if role == 'Admin':
        Admin_panel()
    elif role == 'User':
        User_panel()


def extract_data(column, username):
    con, cur = connect_base()
    cur.execute("""SELECT """ + str(column) + """ FROM user_list WHERE username=(?)""", [username])
    column_raw = cur.fetchall()
    new_column = [i[0] for i in column_raw]
    new_column = new_column[0]
    cur.close()

    return new_column


def try_user(username):
    con, cur = connect_base()
    cur.execute("""SELECT username FROM user_list""")
    users_raw = cur.fetchall()
    con.close()

    users = [i[0] for i in users_raw]

    for i in users:
        if i == username:
            return True
    return False


Login_window()
