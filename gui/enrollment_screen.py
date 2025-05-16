import tkinter as tk
from tkinter import ttk
from controllers.enrollment import get_enrollments, delete_enrollment, add_enrollment
from controllers.course import get_courses
from controllers.user import get_students


def open_enrollment_window(parent):
    """Открыть окно для просмотра, добавления, удаления и редактирования зачислений."""
    enrollment_window = tk.Toplevel(parent)
    enrollment_window.title("Список зачислений")

    columns = ("id", "course_title", "user_name")
    tree = ttk.Treeview(enrollment_window, columns=columns, show="headings")
    tree.heading("id", text="ID")
    tree.heading("course_title", text="Курс")
    tree.heading("user_name", text="Пользователь")
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    users = get_students()
    courses = get_courses()
    user_dict = {user.id: f"{user.first_name} {user.last_name}" for user in users}
    course_dict = {course.id: course.title for course in courses}

    def refresh_table():
        """Обновить данные в таблице."""
        for row in tree.get_children():
            tree.delete(row)
        enrollments = get_enrollments()
        for enrollment in enrollments:
            user_name = user_dict.get(enrollment.user_id, "Неизвестно")
            course_title = course_dict.get(enrollment.course_id, "Неизвестно")
            tree.insert("", tk.END, values=(enrollment.id, course_title, user_name))

    refresh_table()

    tk.Label(enrollment_window, text="Выберите курс:").pack(pady=5)
    course_combobox = ttk.Combobox(enrollment_window, values=list(course_dict.values()), state="readonly")
    course_combobox.pack(pady=5)

    tk.Label(enrollment_window, text="Выберите пользователя:").pack(pady=5)
    user_combobox = ttk.Combobox(enrollment_window, values=list(user_dict.values()), state="readonly")
    user_combobox.pack(pady=5)

    def add_new_enrollment():
        selected_course = course_combobox.get()
        selected_user = user_combobox.get()

        course_id = next((id for id, title in course_dict.items() if title == selected_course), None)
        user_id = next((id for id, name in user_dict.items() if name == selected_user), None)

        if course_id and user_id:
            add_enrollment(course_id, user_id)
            refresh_table()
            course_combobox.set("")
            user_combobox.set("")
        else:
            tk.Label(enrollment_window, text="Выберите корректные данные!", fg="red").pack(pady=5)

    add_enrollment_button = tk.Button(enrollment_window, text="Добавить зачисление", command=add_new_enrollment)
    add_enrollment_button.pack(pady=10)

    def delete_selected_enrollment():
        selected_item = tree.selection()
        if selected_item:
            enrollment_id = tree.item(selected_item, "values")[0]
            delete_enrollment(enrollment_id)
            refresh_table()

    delete_enrollment_button = tk.Button(enrollment_window, text="Удалить зачисление", command=delete_selected_enrollment)
    delete_enrollment_button.pack(pady=10)

    def edit_selected_enrollment():
        selected_item = tree.selection()
        if selected_item:
            enrollment_id = tree.item(selected_item, "values")[0]
            open_edit_enrollment_window(enrollment_window, enrollment_id, refresh_table, course_dict, user_dict)

    edit_enrollment_button = tk.Button(enrollment_window, text="Редактировать зачисление", command=edit_selected_enrollment)
    edit_enrollment_button.pack(pady=10)

    enrollment_window.transient(parent)  
    enrollment_window.grab_set() 
    parent.wait_window(enrollment_window)


def open_edit_enrollment_window(parent, enrollment_id, refresh_callback, course_dict, user_dict):
    """Открыть окно для редактирования зачисления."""
    edit_enrollment_window = tk.Toplevel(parent)
    edit_enrollment_window.title("Редактировать зачисление")

    enrollments = get_enrollments()
    enrollment = next((e for e in enrollments if e.id == int(enrollment_id)), None)

    if not enrollment:
        tk.Label(edit_enrollment_window, text="Зачисление не найдено!", fg="red").pack(pady=10)
        return

    tk.Label(edit_enrollment_window, text="Выберите курс:").pack(pady=5)
    course_combobox = ttk.Combobox(edit_enrollment_window, values=list(course_dict.values()), state="readonly")
    course_combobox.set(course_dict.get(enrollment.course_id, "Неизвестно"))
    course_combobox.pack(pady=5)

    tk.Label(edit_enrollment_window, text="Выберите пользователя:").pack(pady=5)
    user_combobox = ttk.Combobox(edit_enrollment_window, values=list(user_dict.values()), state="readonly")
    user_combobox.set(user_dict.get(enrollment.user_id, "Неизвестно"))
    user_combobox.pack(pady=5)

    def save_changes():
        selected_course = course_combobox.get()
        selected_user = user_combobox.get()

        course_id = next((id for id, title in course_dict.items() if title == selected_course), None)
        user_id = next((id for id, name in user_dict.items() if name == selected_user), None)

        if course_id and user_id:
            delete_enrollment(enrollment_id)  
            add_enrollment(course_id, user_id)
            refresh_callback()
            edit_enrollment_window.destroy()
        else:
            tk.Label(edit_enrollment_window, text="Выберите корректные данные!", fg="red").pack(pady=5)

    save_button = tk.Button(edit_enrollment_window, text="Сохранить", command=save_changes)
    save_button.pack(pady=10)

    edit_enrollment_window.transient(parent)  
    edit_enrollment_window.grab_set() 
    parent.wait_window(edit_enrollment_window)