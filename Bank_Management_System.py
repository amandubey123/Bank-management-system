import customtkinter as ctk
from tkinter import messagebox, simpledialog
import json
import os

ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

class BankSystem:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Colorful Bank Management System")
        self.root.geometry("400x500")
        self.current_user = None
        self.accounts = self.load_accounts()

        self.main_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.login_frame = None
        self.account_frame = None

        self.show_login()

    def load_accounts(self):
        if os.path.exists("accounts.json"):
            with open("accounts.json", "r") as file:
                return json.load(file)
        return {}

    def save_accounts(self):
        with open("accounts.json", "w") as file:
            json.dump(self.accounts, file)

    def show_login(self):
        if self.account_frame:
            self.account_frame.destroy()

        self.login_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.login_frame.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(self.login_frame, text="Welcome to Colorful Bank", font=("Roboto", 24)).pack(pady=20)

        self.username_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Username")
        self.username_entry.pack(pady=10, padx=20)

        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10, padx=20)

        ctk.CTkButton(self.login_frame, text="Login", command=self.login).pack(pady=10)
        ctk.CTkButton(self.login_frame, text="Create Account", command=self.create_account).pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.accounts and self.accounts[username]["password"] == password:
            self.current_user = username
            self.show_account_menu()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def create_account(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        initial_balance = simpledialog.askfloat("Create Account", "Enter initial balance:")

        if username and password and initial_balance is not None:
            if username not in self.accounts:
                self.accounts[username] = {"password": password, "balance": initial_balance}
                self.save_accounts()
                messagebox.showinfo("Success", "Account created successfully")
                self.current_user = username
                self.show_account_menu()
            else:
                messagebox.showerror("Error", "Username already exists")
        else:
            messagebox.showerror("Error", "Invalid input")

    def show_account_menu(self):
        self.login_frame.destroy()
        self.account_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.account_frame.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(self.account_frame, text=f"Welcome, {self.current_user}!", font=("Roboto", 24)).pack(pady=20)

        ctk.CTkButton(self.account_frame, text="Check Balance", command=self.check_balance).pack(pady=10)
        ctk.CTkButton(self.account_frame, text="Deposit", command=self.deposit).pack(pady=10)
        ctk.CTkButton(self.account_frame, text="Withdraw", command=self.withdraw).pack(pady=10)
        ctk.CTkButton(self.account_frame, text="Transfer", command=self.transfer).pack(pady=10)
        ctk.CTkButton(self.account_frame, text="Logout", command=self.logout, fg_color="red", hover_color="dark red").pack(pady=20)

    def check_balance(self):
        balance = self.accounts[self.current_user]["balance"]
        messagebox.showinfo("Balance", f"Your current balance is: ${balance:.2f}")

    def deposit(self):
        amount = simpledialog.askfloat("Deposit", "Enter amount to deposit:")
        if amount is not None and amount > 0:
            self.accounts[self.current_user]["balance"] += amount
            self.save_accounts()
            messagebox.showinfo("Success", f"${amount:.2f} deposited successfully")
        else:
            messagebox.showerror("Error", "Invalid amount")

    def withdraw(self):
        amount = simpledialog.askfloat("Withdraw", "Enter amount to withdraw:")
        if amount is not None and amount > 0:
            if self.accounts[self.current_user]["balance"] >= amount:
                self.accounts[self.current_user]["balance"] -= amount
                self.save_accounts()
                messagebox.showinfo("Success", f"${amount:.2f} withdrawn successfully")
            else:
                messagebox.showerror("Error", "Insufficient funds")
        else:
            messagebox.showerror("Error", "Invalid amount")

    def transfer(self):
        recipient = simpledialog.askstring("Transfer", "Enter recipient's username:")
        amount = simpledialog.askfloat("Transfer", "Enter amount to transfer:")

        if recipient and amount is not None and amount > 0:
            if recipient in self.accounts:
                if self.accounts[self.current_user]["balance"] >= amount:
                    self.accounts[self.current_user]["balance"] -= amount
                    self.accounts[recipient]["balance"] += amount
                    self.save_accounts()
                    messagebox.showinfo("Success", f"${amount:.2f} transferred to {recipient} successfully")
                else:
                    messagebox.showerror("Error", "Insufficient funds")
            else:
                messagebox.showerror("Error", "Recipient not found")
        else:
            messagebox.showerror("Error", "Invalid input")

    def logout(self):
        self.current_user = None
        self.show_login()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    bank_system = BankSystem()
    bank_system.run()

