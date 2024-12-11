import tkinter as tk
from tkinter import messagebox
import csv

class CashCompassApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cash Compass")

        # In-memory storage for income and expense entries
        self.incomes = []
        self.expenses = []

        # Instance variables for entry type (income or expense) and entry fields
        self.entry_type = None  # Initialize entry_type in __init__
        self.amount_entry = None  # Initialize amount_entry
        self.description_entry = None  # Initialize description_entry

        # Main menu
        self.main_menu()

    def main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Cash Compass", font=("Arial", 24)).pack(pady=20)
        tk.Button(self.root, text="Add Income", command=lambda: self.open_add_entry_window('income')).pack(pady=10)
        tk.Button(self.root, text="Add Expense", command=lambda: self.open_add_entry_window('expense')).pack(pady=10)
        tk.Button(self.root, text="View Summary", command=self.open_view_summary_window).pack(pady=10)
        tk.Button(self.root, text="View Entries", command=self.open_view_entries_window).pack(pady=10)
        tk.Button(self.root, text="Export Data", command=self.export_data).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

    def open_add_entry_window(self, entry_type):
        self.entry_type = entry_type  # Set the entry type

        for widget in self.root.winfo_children():
            widget.destroy()

        # Entry window
        tk.Label(self.root, text=f"Add {entry_type.capitalize()}", font=("Arial", 20)).pack(pady=20)

        self.amount_entry = tk.Entry(self.root)  # Initialize amount_entry
        tk.Label(self.root, text="Amount:").pack()
        self.amount_entry.pack(pady=5)

        self.description_entry = tk.Entry(self.root)  # Initialize description_entry
        tk.Label(self.root, text="Description:").pack()
        self.description_entry.pack(pady=5)

        tk.Button(self.root, text="Save", command=self.save_entry).pack(pady=10)
        tk.Button(self.root, text="Cancel", command=self.main_menu).pack(pady=10)

    def save_entry(self):
        amount = self.amount_entry.get()
        description = self.description_entry.get()

        try:
            # Validate amount input
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive.")

            # Save entry
            entry = {"amount": amount, "description": description}

            if self.entry_type == 'income':
                self.incomes.append(entry)
            elif self.entry_type == 'expense':
                self.expenses.append(entry)

            messagebox.showinfo("Success", f"{self.entry_type.capitalize()} added successfully!")
            self.main_menu()

        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def open_view_summary_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        total_income = sum(entry['amount'] for entry in self.incomes)
        total_expenses = sum(entry['amount'] for entry in self.expenses)
        balance = total_income - total_expenses

        tk.Label(self.root, text="Financial Summary", font=("Arial", 20)).pack(pady=20)
        tk.Label(self.root, text=f"Total Income: ${total_income:.2f}").pack(pady=5)
        tk.Label(self.root, text=f"Total Expenses: ${total_expenses:.2f}").pack(pady=5)
        tk.Label(self.root, text=f"Balance: ${balance:.2f}").pack(pady=5)

        tk.Button(self.root, text="Back to Main Menu", command=self.main_menu).pack(pady=20)

    def open_view_entries_window(self, i=None):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="View Entries", font=("Arial", 20)).pack(pady=20)

        # Income entries
        tk.Label(self.root, text="Income Entries", font=("Arial", 16)).pack(pady=10)
        for i, entry in enumerate(self.incomes):
            tk.Label(self.root, text=f"Amount: ${entry['amount']} - Description: {entry['description']}").pack()
            tk.Button(self.root, text="Edit", command=lambda i=i: self.edit_entry('income', i)).pack(pady=5)
            tk.Button(self.root, text="Delete", command=lambda i=i: self.delete_entry('income', i)).pack(pady=5)

        # Expense entries
        tk.Label(self.root, text="Expense Entries", font=("Arial", 16)).pack(pady=10)
        for i, entry in enumerate(self.expenses):
            tk.Label(self.root, text=f"Amount: ${entry['amount']} - Description: {entry['description']}").pack()
            tk.Button(self.root, text="Edit", command=lambda i=i: self.edit_entry('expense', i)).pack(pady=5)
            tk.Button(self.root, text="Delete", command=lambda i=i: self.delete_entry('expense', i)).pack(pady=5)

        tk.Button(self.root, text="Back to Main Menu", command=self.main_menu).pack(pady=20)

    def edit_entry(self, entry_type, entry_index):
        entry = self.incomes[entry_index] if entry_type == 'income' else self.expenses[entry_index]
        self.open_add_entry_window(entry_type)

        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, entry['amount'])
        self.description_entry.delete(0, tk.END)
        self.description_entry.insert(0, entry['description'])

        # Override the save function for editing
        def save_edited_entry():
            try:
                amount = float(self.amount_entry.get())
                if amount <= 0:
                    raise ValueError("Amount must be positive.")
                entry['amount'] = amount
                entry['description'] = self.description_entry.get()

                messagebox.showinfo("Success", f"{entry_type.capitalize()} updated successfully!")
                self.main_menu()
            except ValueError as e:
                messagebox.showerror("Input Error", f"Invalid input: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {e}")

        tk.Button(self.root, text="Save Changes", command=save_edited_entry).pack(pady=10)

    def delete_entry(self, entry_type, entry_index):
        entry = self.incomes[entry_index] if entry_type == 'income' else self.expenses[entry_index]
        confirm = messagebox.askyesno("Delete Entry",
                                      f"Are you sure you want to delete the entry?\nAmount: ${entry['amount']} - Description: {entry['description']}")

        if confirm:
            if entry_type == 'income':
                del self.incomes[entry_index]
            elif entry_type == 'expense':
                del self.expenses[entry_index]

            messagebox.showinfo("Success", f"{entry_type.capitalize()} deleted successfully!")
            self.open_view_entries_window()

    def export_data(self):
        with open('cash_compass_data.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Type", "Amount", "Description"])  # Column headers
            for entry in self.incomes:
                writer.writerow(["Income", entry['amount'], entry['description']])
            for entry in self.expenses:
                writer.writerow(["Expense", entry['amount'], entry['description']])

        messagebox.showinfo("Export Success", "Data has been successfully exported to 'cash_compass_data.csv'.")


if __name__ == "__main__":
    root = tk.Tk()
    app = CashCompassApp(root)
    root.mainloop()