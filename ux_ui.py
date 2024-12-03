from expense import Expense
import tkinter as tk
from tkinter import ttk, messagebox
import calendar
import datetime


class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")

        self.expense_file_path = "expenses.csv"
        self.budget = 0
        self.expenses = []

        # Create the UI components
        self.create_budget_input_ui()
        self.create_expense_input_ui()
        self.create_summary_ui()

    def create_budget_input_ui(self):
        frame = ttk.LabelFrame(self.root, text="Set Budget")
        frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(frame, text="Enter your budget:").grid(row=0, column=0, padx=5, pady=5)
        self.budget_entry = ttk.Entry(frame)
        self.budget_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Set Budget", command=self.set_budget).grid(row=0, column=2, padx=5, pady=5)

    def create_expense_input_ui(self):
        frame = ttk.LabelFrame(self.root, text="Add Expense")
        frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(frame, text="Expense Name:").grid(row=0, column=0, padx=5, pady=5)
        self.expense_name_entry = ttk.Entry(frame)
        self.expense_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
        self.expense_amount_entry = ttk.Entry(frame)
        self.expense_amount_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Category:").grid(row=2, column=0, padx=5, pady=5)
        self.category_var = tk.StringVar()
        self.category_menu = ttk.Combobox(frame, textvariable=self.category_var)
        self.category_menu['values'] = ["Food", "Home", "Utility", "Transportation", "skincare", "Saving", "Others"]
        self.category_menu.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Add Expense", command=self.add_expense).grid(row=3, column=0, columnspan=2, pady=10)

    def create_summary_ui(self):
        frame = ttk.LabelFrame(self.root, text="Expense Summary")
        frame.pack(padx=10, pady=10, fill="x")

        self.summary_text = tk.Text(frame, height=10, state="disabled")
        self.summary_text.pack(padx=5, pady=5, fill="x")

        ttk.Button(frame, text="Update Summary", command=self.update_summary).pack(pady=5)

    def set_budget(self):
        try:
            self.budget = float(self.budget_entry.get())
            messagebox.showinfo("Budget Set", f"Budget set to ${self.budget:.2f}")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the budget.")

    def add_expense(self):
        try:
            name = self.expense_name_entry.get()
            amount = float(self.expense_amount_entry.get())
            category = self.category_var.get()

            if not name or not category:
                raise ValueError("Name and category cannot be empty.")

            new_expense = Expense(name=name, amount=amount, category=category)
            self.save_expense_to_file(new_expense)
            messagebox.showinfo("Expense Added", f"Added expense: {name} (${amount:.2f}) in {category}")
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))

    def save_expense_to_file(self, expense):
        with open(self.expense_file_path, "a") as f:
            f.write(f"{expense.name},{expense.amount},{expense.category}\n")

    def load_expenses_from_file(self):
        expenses = []
        try:
            with open(self.expense_file_path, "r") as f:
                lines = f.readlines()
                for line in lines:
                    name, amount, category = line.strip().split(",")
                    expenses.append(Expense(name=name, amount=float(amount), category=category))
        except FileNotFoundError:
            pass
        return expenses

    def summarize_expenses(self):
        amount_by_category = {}
        total_spent = 0

        for expense in self.expenses:
            total_spent += expense.amount
            if expense.category in amount_by_category:
                amount_by_category[expense.category] += expense.amount
            else:
                amount_by_category[expense.category] = expense.amount

        remaining_budget = self.budget - total_spent
        now = datetime.datetime.now()
        days_in_month = calendar.monthrange(now.year, now.month)[1]
        remaining_days = days_in_month - now.day
        daily_budget = remaining_budget / remaining_days if remaining_days > 0 else 0

        summary = "Expense By Category:\n"
        for category, amount in amount_by_category.items():
            summary += f"  {category}: ${amount:.2f}\n"

        summary += f"\nTotal Spent: ${total_spent:.2f}\n"
        summary += f"Budget Remaining: ${remaining_budget:.2f}\n"
        summary += f"Remaining Days: {remaining_days}\n"
        summary += f"Budget Per Day: ${daily_budget:.2f}\n"

        return summary

    def update_summary(self):
        self.expenses = self.load_expenses_from_file()
        summary_text = self.summarize_expenses()
        self.summary_text.config(state="normal")
        self.summary_text.delete(1.0, "end")
        self.summary_text.insert("end", summary_text)
        self.summary_text.config(state="disabled")


# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
