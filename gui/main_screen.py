import tkinter as tk
from tkinter import ttk
from controllers.user import get_students, delete_student, update_student
from gui.add_user import open_add_user_window
from gui.course_screen import open_course_window
from gui.enrollment_screen import open_enrollment_window


def create_main_screen():
    """Создает главное окно приложения."""
    root = tk.Tk()
    root.title("Список пользователей")

    # Заголовок
    title_label = tk.Label(root, text="Список пользователей", font=("Arial", 16))
    title_label.pack(pady=10)

    # Таблица для отображения пользователей
    columns = ("id", "first_name", "last_name", "email")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    tree.heading("id", text="ID")
    tree.heading("first_name", text="Имя")
    tree.heading("last_name", text="Фамилия")
    tree.heading("email", text="Email")
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Заполнение таблицы данными из базы
    def refresh_table():
        """Обновить данные в таблице."""
        for row in tree.get_children():
            tree.delete(row)
        users = get_students()
        for user in users:
            tree.insert("", tk.END, values=(user.id, user.first_name, user.last_name, user.email))

    refresh_table()

    add_user_button = tk.Button(root, text="Добавить пользователя", command=lambda: open_add_user_window(root, refresh_table))
    add_user_button.pack(pady=5)

    def edit_selected_user():
        selected_item = tree.selection()
        if selected_item:
            user_id = tree.item(selected_item, "values")[0]
            open_edit_user_window(root, user_id, refresh_table)

    edit_user_button = tk.Button(root, text="Редактировать пользователя", command=edit_selected_user)
    edit_user_button.pack(pady=5)

    def delete_selected_user():
        selected_item = tree.selection()
        if selected_item:
            user_id = tree.item(selected_item, "values")[0]
            delete_student(user_id)
            refresh_table()

    delete_user_button = tk.Button(root, text="Удалить пользователя", command=delete_selected_user)
    delete_user_button.pack(pady=5)

    view_courses_button = tk.Button(root, text="Просмотр курсов", command=lambda: open_course_window(root))
    view_courses_button.pack(pady=5)

    view_enrollments_button = tk.Button(root, text="Просмотр зачислений", command=lambda: open_enrollment_window(root))
    view_enrollments_button.pack(pady=5)

    exit_button = tk.Button(root, text="Выход", command=root.destroy)
    exit_button.pack(pady=5)

    root.mainloop()


def open_edit_user_window(parent, user_id, refresh_callback):
    """Открыть окно для редактирования пользователя."""
    edit_user_window = tk.Toplevel(parent)
    edit_user_window.title("Редактировать пользователя")

    users = get_students()
    user = next((u for u in users if u.id == int(user_id)), None)

    if not user:
        tk.Label(edit_user_window, text="Пользователь не найден!", fg="red").pack(pady=10)
        return

    tk.Label(edit_user_window, text="Имя:").grid(row=0, column=0, padx=10, pady=5)
    first_name_entry = tk.Entry(edit_user_window)
    first_name_entry.insert(0, user.first_name)
    first_name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(edit_user_window, text="Фамилия:").grid(row=1, column=0, padx=10, pady=5)
    last_name_entry = tk.Entry(edit_user_window)
    last_name_entry.insert(0, user.last_name)
    last_name_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(edit_user_window, text="Email:").grid(row=2, column=0, padx=10, pady=5)
    email_entry = tk.Entry(edit_user_window)
    email_entry.insert(0, user.email)
    email_entry.grid(row=2, column=1, padx=10, pady=5)

    def save_changes():
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        email = email_entry.get()

        if first_name and last_name and email:
            update_student(user_id, first_name, last_name, email)
            refresh_callback()
            edit_user_window.destroy()
        else:
            tk.Label(edit_user_window, text="Все поля обязательны!", fg="red").grid(row=4, column=0, columnspan=2, pady=5)

    save_button = tk.Button(edit_user_window, text="Сохранить", command=save_changes)
    save_button.grid(row=3, column=0, columnspan=2, pady=10)

    edit_user_window.transient(parent)
    edit_user_window.grab_set() 
    parent.wait_window(edit_user_window)


if __name__ == "__main__":
    create_main_screen()