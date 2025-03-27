import hashlib
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from flask import Flask, send_from_directory

class Bill:
    def __init__(self, amount, date, file_path):
        self.amount = amount
        self.date = date
        self.file_path = file_path
        self.hash = self._calculate_hash()

    def _calculate_hash(self):
        """Calculate SHA-256 hash of the file only (ignoring date)."""
        try:
            with open(self.file_path, 'rb') as f:
                file_content = f.read()
            return hashlib.sha256(file_content).hexdigest()  # Hash file only
        except FileNotFoundError:
            return None

    def __eq__(self, other):
        """Check if two bills are identical based on the file hash only."""
        if isinstance(other, Bill):
            return self.hash == other.hash
        return False

    def __str__(self):
        return f"Bill(Amount: {self.amount}, Date: {self.date}, File: {self.file_path}, Hash: {self.hash})"

    def to_dict(self):
        return {"amount": self.amount, "date": self.date, "file_hash": self.hash}

class DuplicateBillFinder:
    def __init__(self):
        self.bill_hashes = set()  # Store file hashes to detect duplicates

    def add_bill(self, amount, date_str, file_path):
        try:
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            bill = Bill(amount, date, file_path)

            if bill.hash is None:
                messagebox.showerror("Error", f"File not found: {file_path}")
                return False

            if bill.hash in self.bill_hashes:
                messagebox.showwarning("Duplicate Detected", f"Duplicate bill found!\nAmount: {amount}, File: {file_path}")
                return False  # Stop adding duplicate file

            self.bill_hashes.add(bill.hash)
            print(f"Bill added successfully: {bill}")
            return True

        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return False

class BillApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Duplicate Bill Finder")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")

        self.finder = DuplicateBillFinder()

        style = ttk.Style()
        style.configure("TButton", padding=6, font=('Arial', 10), background="#4CAF50", foreground="white")
        style.configure("TLabel", font=('Arial', 10), background="#f0f0f0")
        style.configure("TEntry", font=('Arial', 10))

        ttk.Label(root, text="Amount:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.amount_entry = ttk.Entry(root)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(root, text="Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.date_entry = ttk.Entry(root)
        self.date_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(root, text="Bill File:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.file_path_label = ttk.Label(root, text="No file selected")
        self.file_path_label.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        ttk.Button(root, text="Browse", command=self.browse_file).grid(row=2, column=2, padx=5, pady=5)
        ttk.Button(root, text="Add Bill", command=self.add_bill).grid(row=3, column=1, pady=10)

        self.log_text = tk.Text(root, height=10, width=50, state=tk.DISABLED, bg="#e0e0e0")
        self.log_text.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path_label.config(text=file_path)

    def add_bill(self):
        amount = self.amount_entry.get()
        date_str = self.date_entry.get()
        file_path = self.file_path_label.cget("text")

        try:
            amount = int(amount)
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a number.")
            return

        if file_path == "No file selected":
            messagebox.showerror("Error", "Please select a bill file.")
            return

        success = self.finder.add_bill(amount, date_str, file_path)

        if success:
            self.log_message(f"Bill added successfully: Amount: {amount}, Date: {date_str}, File: {file_path}")
        else:
            self.log_message(f"Duplicate bill detected: Amount: {amount}, Date: {date_str}, File: {file_path}")

    def log_message(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = BillApp(root)
    root.mainloop()

app = Flask(__name__, static_folder='static')

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')
