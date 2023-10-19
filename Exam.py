


from abc import ABC, abstractmethod

class Account(ABC):
    accounts = []
    account_number_counter = 1000

    def __init__(self, name, email, address, account_type):

        self.name = name

        self.email = email

        self.address = address

        self.account_type = account_type

        self.account_number = Account.account_number_counter

        Account.account_number_counter += 1

        self.balance = 0

        self.transaction_history = []

        self.loan_count = 0  

        Account.accounts.append(self)


    @abstractmethod
    def show_info(self):
        pass

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(f"Deposited ${amount}")
            print(f"Deposited ${amount}. New balance: ${self.balance}")

        else:
            print("Invalid deposit amount")

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            self.transaction_history.append(f"Withdrew ${amount}")
            print(f"Withdrew ${amount}. New balance: ${self.balance}")

        else:
            print("Invalid withdrawal amount")

    def check_balance(self):
        return self.balance

    def check_transaction_history(self):
        print("Transaction History:")
        for transaction in self.transaction_history:
            print(transaction)

    def transfer(self, recipient_account, amount):
        if recipient_account in Account.accounts:
            if self.balance >= amount:
                self.withdraw(amount)
                recipient_account.deposit(amount)
                self.transaction_history.append(f"Transferred ${amount} to account {recipient_account.account_number}")
                print(f"Transferred ${amount} to account {recipient_account.account_number}")
            else:
                print("Withdrawal amount exceeded")
        else:
            print("Account does not exist")

class SavingsAccount(Account):
    def __init__(self, name, email, address):
        super().__init__(name, email, address, "Savings")

    def show_info(self):
        print(f"Account Type: {self.account_type}")
        print(f"Name: {self.name}")
        print(f"Account Number: {self.account_number}")
        print(f"Current Balance: ${self.balance}")

class CurrentAccount(Account):
    def __init__(self, name, email, address):
        super().__init__(name, email, address, "Current")

    def show_info(self):
        print(f"Account Type: {self.account_type}")
        print(f"Name: {self.name}")
        print(f"Account Number: {self.account_number}")
        print(f"Current Balance: ${self.balance}")

class Admin:
    def create_account(self, name, email, address, account_type):
        account_type = account_type.lower()  # Convert to lowercase for case-insensitivity
        if account_type == "savings":
            account = SavingsAccount(name, email, address)
        elif account_type == "current":
            account = CurrentAccount(name, email, address)
        else:
            print("Invalid account type")


    def delete_account(self, account):
        if account in Account.accounts:
            Account.accounts.remove(account)
            print("Account deleted")

    def see_all_accounts(self):
        print("All User Accounts:")
        for account in Account.accounts:
            account.show_info()
            print()

    def total_balance(self):
        total = sum(account.balance for account in Account.accounts)
        print(f"Total Available Balance in the bank: ${total}")

admin = Admin()
while True:
    print("\nChoose User Type:")
    print("1. User")
    print("2. Admin")
    print("3. Exit")
    user_type = input("Enter your choice (1/2/3): ")

    if user_type == "1":
        if not Account.accounts:
            print("No user accounts found. Please contact the admin to create an account.")
            continue

        account_number = int(input("Enter your account number: "))
        user_account = None
        for account in Account.accounts:
            if account.account_number == account_number:
                user_account = account
                break

        if user_account is None:
            print("Account not found.")
        else:
            print(f"Welcome, {user_account.name}!")

            while True:
                print("\nUser Menu:")
                print("1. Deposit")
                print("2. Withdraw")
                print("3. Check Balance")
                print("4. Transaction History")
                print("5. Transfer Money")
                print("6. Logout")
                choice = input("Enter your choice (1/2/3/4/5/6): ")

                if choice == "1":
                    amount = int(input("Enter deposit amount: $"))
                    user_account.deposit(amount)
                elif choice == "2":
                    amount = int(input("Enter withdrawal amount: $"))
                    user_account.withdraw(amount)
                elif choice == "3":
                    balance = user_account.check_balance()
                    print(f"Current Balance: ${balance}")
                elif choice == "4":
                    user_account.check_transaction_history()
                elif choice == "5":
                    recipient_account_number = int(input("Enter recipient's account number: "))
                    recipient_account = None
                    for account in Account.accounts:
                        if account.account_number == recipient_account_number:
                            recipient_account = account
                            break
                    if recipient_account:
                        amount = int(input("Enter transfer amount: $"))
                        user_account.transfer(recipient_account, amount)
                    else:
                        print("Recipient account not found.")
                elif choice == "6":
                    print("Logged out.")
                    break
                else:
                    print("Invalid choice. Please try again.")

    elif user_type == "2":
        print("\nAdmin Menu:")
        print("1. Create Account")
        print("2. Delete Account")
        print("3. See All Accounts")
        admin_choice = input("Enter your choice (1/2/3): ")

        if admin_choice == "1":
            name = input("Enter user's name: ")
            email = input("Enter user's email: ")
            address = input("Enter user's address: ")
            account_type = input("Enter account type (Savings/Current): ")
            admin.create_account(name, email, address, account_type)
        elif admin_choice == "2":
            account_number = int(input("Enter account number to delete: "))
            for account in Account.accounts:
                if account.account_number == account_number:
                    admin.delete_account(account)
                    print("Account deleted.")
                    break
            else:
                print("Account not found.")
        elif admin_choice == "3":
            admin.see_all_accounts()
        else:
            print("Invalid choice.")
