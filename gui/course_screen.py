import tkinter as tk
from tkinter import ttk
from controllers.course import get_courses, add_course, delete_course
from controllers.user import get_students


def open_course_window(parent):
    """Открыть окно для просмотра, добавления, удаления и редактирования курсов."""
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
        """Обновить данные в таблице."""
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

    def edit_selected_course():
        selected_item = tree.selection()
        if selected_item:
            course_id = tree.item(selected_item, "values")[0]
            open_edit_course_window(course_window, course_id, refresh_table)

    edit_course_button = tk.Button(course_window, text="Редактировать курс", command=edit_selected_course)
    edit_course_button.pack(pady=10)

    course_window.transient(parent)
    course_window.grab_set()
    parent.wait_window(course_window)


def open_edit_course_window(parent, course_id, refresh_callback):
    """Открыть окно для редактирования курса."""
    edit_course_window = tk.Toplevel(parent)
    edit_course_window.title("Редактировать курс")

    courses = get_courses()
    course = next((c for c in courses if c.id == int(course_id)), None)

    if not course:
        tk.Label(edit_course_window, text="Курс не найден!", fg="red").pack(pady=10)
        return

    users = get_students()
    user_dict = {user.id: f"{user.first_name} {user.last_name}" for user in users}
    user_options = {f"{user.first_name} {user.last_name} (ID: {user.id})": user.id for user in users}

    tk.Label(edit_course_window, text="Название курса:").grid(row=0, column=0, padx=10, pady=5)
    title_entry = tk.Entry(edit_course_window)
    title_entry.insert(0, course.title)
    title_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(edit_course_window, text="Автор курса:").grid(row=1, column=0, padx=10, pady=5)
    user_combobox = ttk.Combobox(edit_course_window, values=list(user_options.keys()), state="readonly")
    current_author = user_dict.get(course.author_id, "Неизвестно")
    user_combobox.set(current_author)
    user_combobox.grid(row=1, column=1, padx=10, pady=5)

    def save_changes():
        title = title_entry.get()
        selected_user = user_combobox.get()
        author_id = user_options.get(selected_user)

        if title and author_id:
            delete_course(course_id)
            add_course(title, author_id)
            refresh_callback()
            edit_course_window.destroy()
        else:
            tk.Label(edit_course_window, text="Введите корректные данные!", fg="red").grid(row=3, column=0, columnspan=2, pady=5)

    save_button = tk.Button(edit_course_window, text="Сохранить", command=save_changes)
    save_button.grid(row=2, column=0, columnspan=2, pady=10)

    edit_course_window.transient(parent)
    edit_course_window.grab_set()
    parent.wait_window(edit_course_window)