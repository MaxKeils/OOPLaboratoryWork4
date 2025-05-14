import tkinter as tk
from tkinter import ttk
from controllers.course import get_courses, add_course, delete_course
from controllers.user import get_students 

def open_course_window(parent):
    """Открыть окно для просмотра и добавления курсов."""
    course_window = tk.Toplevel(parent)
    course_window.title("Список курсов")

    columns = ("id", "title", "author_name")
    tree = ttk.Treeview(course_window, columns=columns, show="headings")
    tree.heading("id", text="ID")
    tree.heading("title", text="Название")
    tree.heading("author_name", text="Автор")
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    users = get_students()
    user_dict = {user.id: f"{user.first_name} {user.last_name}" for user in users}

    def refresh_table():
        for row in tree.get_children():
            tree.delete(row)
        courses = get_courses()
        for course in courses:
            author_name = user_dict.get(course.author_id, "Неизвестно")
            tree.insert("", tk.END, values=(course.id, course.title, author_name))

    refresh_table()

    tk.Label(course_window, text="Название курса:").pack(pady=5)
    title_entry = tk.Entry(course_window)
    title_entry.pack(pady=5)

    tk.Label(course_window, text="Автор курса:").pack(pady=5)

    user_options = {f"{user.first_name} {user.last_name} (ID: {user.id})": user.id for user in users}
    user_combobox = ttk.Combobox(course_window, values=list(user_options.keys()), state="readonly")
    user_combobox.pack(pady=5)

    def add_new_course():
        title = title_entry.get()
        selected_user = user_combobox.get()
        if title and selected_user:
            author_id = user_options[selected_user]
            add_course(title, author_id)
            refresh_table()
            title_entry.delete(0, tk.END)
            user_combobox.set("")
        else:
            tk.Label(course_window, text="Введите корректные данные!", fg="red").pack(pady=5)

    add_course_button = tk.Button(course_window, text="Добавить курс", command=add_new_course)
    add_course_button.pack(pady=10)

    def delete_selected_course():
        selected_item = tree.selection()
        if selected_item:
            course_id = tree.item(selected_item, "values")[0]
            delete_course(course_id)
            refresh_table()

    delete_course_button = tk.Button(course_window, text="Удалить курс", command=delete_selected_course)
    delete_course_button.pack(pady=10)

    course_window.transient(parent)
    course_window.grab_set()
    parent.wait_window(course_window)