import tkinter as tk
from tkinter import ttk
from controllers.user import get_students, delete_student
from gui.add_user import open_add_user_window  
from gui.course_screen import open_course_window
from gui.enrollment_screen import open_enrollment_window 


def create_main_screen():
    root = tk.Tk()
    root.title("Список пользователей")

    title_label = tk.Label(root, text="Список пользователей", font=("Arial", 16))
    title_label.pack(pady=10)

    columns = ("id", "first_name", "last_name", "email")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    tree.heading("id", text="ID")
    tree.heading("first_name", text="Имя")
    tree.heading("last_name", text="Фамилия")
    tree.heading("email", text="Email")
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def refresh_table():
        for row in tree.get_children():
            tree.delete(row)
        users = get_students()
        for user in users:
            tree.insert("", tk.END, values=(user.id, user.first_name, user.last_name, user.email))

    refresh_table()

    add_user_button = tk.Button(root, text="Добавить пользователя", command=lambda: open_add_user_window(root, refresh_table))
    add_user_button.pack(pady=5)

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


if __name__ == "__main__":
    create_main_screen()