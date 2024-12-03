from ux_ui import ExpenseTrackerApp
from password import hash_password
import tkinter as tk
from tkinter import ttk, messagebox
import os

PASSWORD_FILE = "password.txt"


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")

        # Login UI
        ttk.Label(self.root, text="Enter your password:").pack(pady=50)
        self.password_entry = ttk.Entry(self.root, show="*", width=50)
        self.password_entry.pack(pady=20)

        ttk.Button(self.root, text="Login", command=self.verify_password).pack(pady=50)

    def verify_password(self):
        entered_password = self.password_entry.get()

        if not os.path.exists(PASSWORD_FILE):
            messagebox.showerror("Error", "No password set. Please create one.")
            self.root.destroy()
            return

        with open(PASSWORD_FILE, "r") as f:
            stored_password = f.read().strip()

        if hash_password(entered_password) == stored_password:
            messagebox.showinfo("Success", "Login successful!")
            self.root.destroy()  # Close the login window

            # Open the Expense Tracker window
            main_window = tk.Tk()
            ExpenseTrackerApp(main_window)
            main_window.mainloop()
        else:
            messagebox.showerror("Error", "Incorrect password.")


# Main Application
if __name__ == "__main__":
    if not os.path.exists(PASSWORD_FILE):
        print("No password found. Please set one first by running the auth setup.")
    else:
        root = tk.Tk()
        LoginApp(root)
        root.mainloop()
