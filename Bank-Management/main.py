"""Manages Bank Accounts and Bank operations"""

import json
import os

DATA_FILE = "bank_data.json"

class BankAccount:
    """A Bank Account"""

    def __init__(self, account_id: int, name: str, age: int, nid: str, balance: float = 0.0) -> None:
        self.account_id = account_id
        self.name = name
        self.age = age
        self.nid = nid
        self.balance = balance

    def deposit(self, amount: float) -> bool:
        if amount <= 0:
            return False
        self.balance += amount
        return True

    def withdraw(self, amount: float) -> bool:
        if amount <= 0 or amount > self.balance:
            return False
        self.balance -= amount
        return True

    def get_balance(self) -> float:
        return self.balance

    def to_dict(self) -> dict:
        return {
            "account_id": self.account_id,
            "name": self.name,
            "age": self.age,
            "nid": self.nid,
            "balance": self.balance,
        }

    @staticmethod
    def from_dict(data: dict) -> "BankAccount":
        return BankAccount(
            account_id=data["account_id"],
            name=data["name"],
            age=data["age"],
            nid=data["nid"],
            balance=data.get("balance", 0.0),
        )


class Bank:
    """A Bank management system"""

    def __init__(self):
        self.accounts = {}
        self.next_id = 1
        self.load()

    def load(self):
        if not os.path.exists(DATA_FILE):
            return
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            records = data.get("accounts", [])
            self.accounts = {rec["account_id"]: BankAccount.from_dict(rec) for rec in records}
            self.next_id = max(self.accounts.keys(), default=0) + 1
        except (json.JSONDecodeError, OSError):
            print("Warning: Failed to load bank data. Starting with an empty bank.")
            self.accounts = {}
            self.next_id = 1

    def save(self):
        payload = {"accounts": [acc.to_dict() for acc in self.accounts.values()]}
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

    def create_account(self, name: str, age: int, nid: str, initial_balance: float = 0.0) -> BankAccount:
        account = BankAccount(self.next_id, name.strip(), age, nid.strip(), float(initial_balance))
        self.accounts[account.account_id] = account
        self.next_id += 1
        self.save()
        return account

    def get_account(self, account_id: int) -> BankAccount | None:
        return self.accounts.get(account_id)

    def delete_account(self, account_id: int) -> bool:
        if account_id in self.accounts:
            del self.accounts[account_id]
            self.save()
            return True
        return False

    def transfer(self, from_id: int, to_id: int, amount: float) -> bool:
        if from_id == to_id or amount <= 0:
            return False
        from_acc = self.get_account(from_id)
        to_acc = self.get_account(to_id)
        if not from_acc or not to_acc or from_acc.balance < amount:
            return False
        from_acc.withdraw(amount)
        to_acc.deposit(amount)
        self.save()
        return True

    def list_accounts(self) -> list[BankAccount]:
        return sorted(self.accounts.values(), key=lambda x: x.account_id)


def _input_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid number. Please try again.")


def _input_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid integer. Please try again.")


def print_menu():
    print("\n=== Bank Management System ===")
    print("1. Create account")
    print("2. View account")
    print("3. Deposit")
    print("4. Withdraw")
    print("5. Transfer")
    print("6. List all accounts")
    print("7. Delete account")
    print("0. Exit")


def run_cli():
    bank = Bank()

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            print("-- Create Account --")
            name = input("Name: ").strip()
            age = _input_int("Age: ")
            nid = input("NID: ").strip()
            initial_balance = _input_float("Initial deposit: ")
            account = bank.create_account(name, age, nid, initial_balance)
            print(f"Created account #{account.account_id} for {account.name} with balance {account.balance:.2f}")

        elif choice == "2":
            print("-- View Account --")
            account_id = _input_int("Account ID: ")
            account = bank.get_account(account_id)
            if account:
                print(f"ID: {account.account_id}, Name: {account.name}, Age: {account.age}, NID: {account.nid}, Balance: {account.balance:.2f}")
            else:
                print("Account not found.")

        elif choice == "3":
            print("-- Deposit --")
            account_id = _input_int("Account ID: ")
            amount = _input_float("Amount: ")
            account = bank.get_account(account_id)
            if account and account.deposit(amount):
                bank.save()
                print(f"Deposited {amount:.2f}. New balance: {account.balance:.2f}")
            else:
                print("Deposit failed. Check account ID and amount.")

        elif choice == "4":
            print("-- Withdraw --")
            account_id = _input_int("Account ID: ")
            amount = _input_float("Amount: ")
            account = bank.get_account(account_id)
            if account and account.withdraw(amount):
                bank.save()
                print(f"Withdrew {amount:.2f}. New balance: {account.balance:.2f}")
            else:
                print("Withdrawal failed. Check account ID, available balance, and amount.")

        elif choice == "5":
            print("-- Transfer --")
            from_id = _input_int("From Account ID: ")
            to_id = _input_int("To Account ID: ")
            amount = _input_float("Amount: ")
            if bank.transfer(from_id, to_id, amount):
                print("Transfer successful.")
            else:
                print("Transfer failed. Check IDs and balance.")

        elif choice == "6":
            print("-- All Accounts --")
            accounts = bank.list_accounts()
            if not accounts:
                print("No accounts found.")
            for acc in accounts:
                print(f"ID: {acc.account_id}, Name: {acc.name}, Balance: {acc.balance:.2f}")

        elif choice == "7":
            print("-- Delete Account --")
            account_id = _input_int("Account ID: ")
            if bank.delete_account(account_id):
                print("Account deleted.")
            else:
                print("Account not found.")

        elif choice == "0":
            print("Exiting. Goodbye!")
            break

        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    run_cli()
    
