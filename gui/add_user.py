import tkinter as tk
from controllers.user import add_student


def open_add_user_window(parent, refresh_callback):
    add_user_window = tk.Toplevel(parent)
    add_user_window.title("Добавить пользователя")

    tk.Label(add_user_window, text="Имя:").grid(row=0, column=0, padx=10, pady=5)
    first_name_entry = tk.Entry(add_user_window)
    first_name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(add_user_window, text="Фамилия:").grid(row=1, column=0, padx=10, pady=5)
    last_name_entry = tk.Entry(add_user_window)
    last_name_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(add_user_window, text="Email:").grid(row=2, column=0, padx=10, pady=5)
    email_entry = tk.Entry(add_user_window)
    email_entry.grid(row=2, column=1, padx=10, pady=5)

    def save_user():
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        email = email_entry.get()

        if first_name and last_name and email:
            add_student(first_name, last_name, email)
            refresh_callback() 
            add_user_window.destroy()
        else:
            tk.Label(add_user_window, text="Все поля обязательны!", fg="red").grid(row=4, column=0, columnspan=2, pady=5)

    save_button = tk.Button(add_user_window, text="Сохранить", command=save_user)
    save_button.grid(row=3, column=0, columnspan=2, pady=10)

    add_user_window.transient(parent)
    add_user_window.grab_set()
    parent.wait_window(add_user_window)