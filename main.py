import hashlib
from classes import Customer, SavingsAccount, CheckingAccount
from classes import pretty_print


class BankSystem:
    """
    A simple banking system with customer management, account handling,
    and transaction tracking.

    Attributes:
        customers (dict): A dictionary containing customer information.
        accounts (dict): A dictionary containing account information.
        transactions (dict): A dictionary containing transaction information.
        current_user (str): The ID of the currently logged-in user.
        admin_password (str): The password for admin access.
    """
    def __init__(self):
        """
        Initializes the BankSystem with empty dictionaries for customers,
        accounts, and transactions. Sets the current_user to None and defines
        the admin password.
        """
        self.customers = {}
        self.accounts = {}
        self.transactions = {}
        self.current_user = None
        self.admin_password = "admin"

    def login(self, login: str, password: str):
        """
        Logs in a customer or admin based on provided credentials.

        Args:
            login (str): The login of the customer attempting to login.
            password (str): The password provided for authentication.

        Returns:
            None
        """
        if login in self.customers:
            customer = self.customers[login]
            if customer.password == hashlib.sha256(password.encode()).hexdigest():
                self.current_user = login
                pretty_print("Login successful.")
            else:
                pretty_print("Incorrect password.")
        else:
            pretty_print("Login not found.")

    def admin_login(self, password: str):
        """
        Logs in the admin with the provided password.

        Args:
            password (str): The password provided for admin authentication.

        Returns:
            None
        """
        if password == self.admin_password:
            self.current_user = "admin"
            pretty_print("Admin login successful.")
        else:
            pretty_print("Incorrect admin password.")

    def logout(self):
        """
        Logs out the currently logged-in user.

        Returns:
            None
        """
        self.current_user = None
        pretty_print("Logged out successfully.")

    def load_data(self):
        """
        Loads data from files into the BankSystem's dictionaries.

        Returns:
            None
        """
        # Load customers data
        with open("data/customers.txt", "r") as file:
            for line in file:
                customer_id, name, age, login, password = line.strip().split(",")
                self.customers[login] = Customer(customer_id, name, int(age), login, password)

        # Load accounts data
        with open("data/accounts.txt", "r") as file:
            for line in file:
                account_line = line.strip().split(",")
                if len(account_line) == 4:
                    account_id, customer_id, account_type, balance = account_line
                    self.accounts[account_id] = CheckingAccount(account_id, customer_id, float(balance))
                if len(account_line) == 5:
                    account_id, customer_id, account_type, balance, monthly_withdrawals = account_line
                    self.accounts[account_id] = SavingsAccount(account_id, customer_id, float(balance), int(monthly_withdrawals))

        # Load transactions data
        with open("data/accountsTransactions.txt", "r") as file:
            for line in file:
                transaction_line = line.strip().split(",")
                if len(transaction_line) == 5:
                    account_id, transaction_id, amount, transaction_type, transaction_status = transaction_line
                    self.transactions.setdefault(account_id, []).append((transaction_id, float(amount), transaction_type, transaction_status))
                if len(transaction_line) == 6:
                    account_id, transaction_id, recipient_account_id, amount, transaction_type, transaction_status = transaction_line
                    self.transactions.setdefault(account_id, []).append((transaction_id, recipient_account_id, float(amount), transaction_type, transaction_status))


    def save_data(self):
        """
        Saves data from the BankSystem's dictionaries into files.

        Returns:
            None
        """
        # Save customers data
        with open("data/customers.txt", "w") as file:
            for customer in self.customers.values():
                file.write(f"{customer.customer_id},{customer.name},{customer.age},{customer.login},{customer.password}\n")

        # Save accounts data
        with open("data/accounts.txt", "w") as file:
            for account in self.accounts.values():
                if isinstance(account, SavingsAccount):
                    file.write(f"{account.account_id},{account.customer_id},Savings,{account.balance},{account.monthly_withdrawals}\n")
                else:
                    file.write(f"{account.account_id},{account.customer_id},Checking,{account.balance}\n")

        # Save transactions data
        with open("data/accountsTransactions.txt", "w") as file:
            for account_id, transactions in self.transactions.items():
                for transaction in transactions:
                    if len(transaction) == 4:
                        transaction_id, amount, transaction_type, transaction_status = transaction
                        file.write(f"{account_id},{transaction_id},{amount},{transaction_type},{transaction_status}\n")
                    if len(transaction) == 5:
                        transaction_id, recipient_account_id, amount, transaction_type, transaction_status = transaction
                        file.write(f"{account_id},{transaction_id},{recipient_account_id},{amount},{transaction_type},{transaction_status}\n")


    def create_customer(self, name: str, age: int, login: str, password: str):
        """
        Creates a new customer and adds them to the system.

        Args:
            name (str): The name of the new customer.
            age (int): The age of the new customer.
            login (str): The login for the new customer.
            password (str): The password for the new customer.

        Returns:
            None
        """
        customer_id = str(len(self.customers) + 1)

        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Store customer data
        self.customers[login] = Customer(customer_id, name, age, login, hashed_password)

        # Save customer data to file
        with open("data/customers.txt", "a") as file:
            file.write(f"{customer_id},{name},{age},{login},{hashed_password}\n")

        pretty_print("Customer created successfully.")

    def create_account(self, customer_id: str, account_type: str):
        """
        Creates a new account for an existing customer.

        Args:
            customer_id (str): The customer ID of the customer for whom the account is created.
            account_type (str): The type of account to be created (Savings or Checking).

        Returns:
            Account: The newly created account object.
        """
        flag = False
        for customer in self.customers:
            if customer_id == self.customers[customer].customer_id:
                flag = True
                found_customer = self.customers[customer]
        if flag == False:
            pretty_print("Customer ID not found.")
            return None

        # Generate a unique account ID
        account_id = str(len(self.accounts) + 1)

        # Checking age restrictions
        if (account_type == "Savings" and found_customer.age < 14) or (account_type == "Checking" and found_customer.age < 18):
            pretty_print("You do not meet the age requirement for this account type.")
            return None
        
        # Create a new account based on the specified account type
        if account_type == "Savings":
            new_account = SavingsAccount(account_id, customer_id)
        elif account_type == "Checking":
            new_account = CheckingAccount(account_id, customer_id)
        else:
            pretty_print("Invalid account type.")
            return None

        # Add the new account to the accounts dictionary
        self.accounts[account_id] = new_account

        pretty_print(f"{account_type} account created successfully.")
        return new_account

    def view_transactions(self, account_id: str):
        """
        Displays the transaction history for a given account.

        Args:
            account_id (str): The ID of the account to view transactions for.

        Returns:
            None
        """
        if self.current_user is None:
            pretty_print("Please login to perform operations.")
            return

        if account_id not in self.accounts:
            pretty_print("Account ID not found.")
            return
        
        account = self.accounts[account_id]
        if self.current_user != "admin" and account.customer_id != self.customers[self.current_user].customer_id:
            pretty_print("You are not authorized to perform operations on this account.")
            return
        
        if account_id not in self.transactions:
            pretty_print("No transactions found for this account.")
            return
        print("\n-----------------------------------")
        print(f"Transaction history for Account ID: {account_id}")
        for transaction in self.transactions[account_id]:
            if len(transaction) == 4:
                transaction_id, amount, transaction_type, status = transaction
                print(f"Transaction ID: {transaction_id}, Amount: {amount}, Type: {transaction_type}, Status: {status}")
            if len(transaction) == 5:
                transaction_id, recipient_account_id, amount, transaction_type, status = transaction
                print(f"Transaction ID: {transaction_id}, Recipient ID: {recipient_account_id}, Amount: {amount}, Type: {transaction_type}, Status: {status}")
        print("-----------------------------------")

    def perform_operations(self, account_id: str):
        """
        Allows the user to perform operations such as deposit, withdrawal, and transfer.

        Args:
            account_id (str): The ID of the account on which operations are performed.

        Returns:
            None
        """
        if self.current_user is None:
            pretty_print("Please login to perform operations.")
            return

        if account_id not in self.accounts:
            pretty_print("Account ID not found.")
            return
        
        account = self.accounts[account_id]
        if self.current_user != "admin" and account.customer_id != self.customers[self.current_user].customer_id:
            pretty_print("You are not authorized to perform operations on this account.")
            return

        transaction_id = str(len(self.transactions.get(account_id, [])) + 1)
        pretty_print(f"Performing operations for Account ID: {account_id}")

        # Operations for Savings Account
        if isinstance(account, SavingsAccount):
            pretty_print("1. Deposit\n2. Withdrawal\n3. Transfer\n")
            choice = input("Enter your choice: ")
            if choice == "1":
                amount = float(input("Enter the amount to deposit: "))
                if account.deposit(amount) == True:
                    self.transactions.setdefault(account_id, []).append((transaction_id, amount, "deposit", "COMPLETE"))
                    pretty_print("Deposit successful.")
                else:
                    self.transactions.setdefault(account_id, []).append((transaction_id, amount, "deposit", "ABORTED"))
                    pretty_print("Operation aborted.")
            
            elif choice == "2":
                amount = float(input("Enter the amount to withdraw: "))
                if account.withdrawal(amount) == True:
                    self.transactions.setdefault(account_id, []).append((transaction_id, amount, "withdrawal", "COMPLETE"))
                    pretty_print("Withdrawal successful.")
                else:
                    self.transactions.setdefault(account_id, []).append((transaction_id, amount, "withdrawal", "ABORTED"))
                    pretty_print("Operation aborted.")
                    
            elif choice == "3":
                recipient_account_id = input("Enter the recipient account ID: ")
                if recipient_account_id not in self.accounts:
                    pretty_print("Recipient account ID not found.")
                    return
                recipient_account = self.accounts[recipient_account_id]
                amount = float(input("Enter the amount to transfer: "))
                if account.transfer(amount, recipient_account) == True:
                    self.transactions.setdefault(account_id, []).append((transaction_id, recipient_account_id, amount, "transfer", "COMPLETE"))
                    pretty_print("Transfer successful.")
                else:
                    self.transactions.setdefault(account_id, []).append((transaction_id, recipient_account_id, amount, "transfer", "ABORTED"))
                    pretty_print("Operation aborted.")
            else:
                pretty_print("Invalid choice.")
        # Operations for Checking Account
        elif isinstance(account, CheckingAccount):
            
            pretty_print("1. Deposit\n2. Withdrawal\n3. Transfer")
            
            choice = input("Enter your choice: ")
            if choice == "1":
                amount = float(input("Enter the amount to deposit: "))
                if account.deposit(amount) == True:
                    self.transactions.setdefault(account_id, []).append((transaction_id, amount, "deposit", "COMPLETE"))
                    pretty_print("Deposit successful.")
                    
                else:
                    self.transactions.setdefault(account_id, []).append((transaction_id, amount, "deposit", "ABORTED"))
                    pretty_print("Operation aborted.")
                    
            elif choice == "2":
                amount = float(input("Enter the amount to withdraw: "))
                if account.withdrawal(amount) == True:
                    self.transactions.setdefault(account_id, []).append((transaction_id, amount, "withdrawal", "COMPLETE"))
                    pretty_print("Withdrawal successful.")
                else:
                    self.transactions.setdefault(account_id, []).append((transaction_id, amount, "withdrawal", "ABORTED"))
                    pretty_print("Operation aborted.")

            elif choice == "3":
                recipient_account_id = input("Enter the recipient account ID: ")
                if recipient_account_id not in self.accounts:
                    pretty_print("Recipient account ID not found.")
                    return
                recipient_account = self.accounts[recipient_account_id]
                amount = float(input("Enter the amount to transfer: "))
                if account.transfer(amount, recipient_account) == True:
                    self.transactions.setdefault(account_id, []).append((transaction_id, recipient_account_id, amount, "transfer", "COMPLETE"))
                    pretty_print("Transfer successful.")
                else:
                    self.transactions.setdefault(account_id, []).append((transaction_id, recipient_account_id, amount, "transfer", "ABORTED"))
                    pretty_print("Operation aborted.")
            else:
                pretty_print("Invalid choice.")
                
    def check_balance(self, account_id: str):
        """
        Checks and displays the balance of a specified account.

        Args:
            account_id (str): The ID of the account to check balance for.

        Returns:
            None
        """
        
        if self.current_user is None:
            pretty_print("Please login to check balance.")
            return

        if account_id not in self.accounts:
            pretty_print("Account ID not found.")
            return
        
        account = self.accounts[account_id]
        if self.current_user != "admin" and account.customer_id != self.customers[self.current_user].customer_id:
            pretty_print("You are not authorized to check balance of this account.")
            return
        account.show_balance()
        

    def delete_account(self, account_id: str):
        """
        Deletes the specified account from the system.

        Args:
            account_id (str): The ID of the account to be deleted.

        Returns:
            None
        """
        if account_id not in self.accounts:
            pretty_print("Account ID not found.")
            return
        # Remove the account from the accounts dictionary
        del self.accounts[account_id]

        # Remove related transactions
        if account_id in self.transactions:
            del self.transactions[account_id]

        pretty_print(f"Account ID: {account_id} deleted successfully.")

    def start(self):
        """
        Starts the BankSystem application, allowing users to login, create customers,
        create accounts, view transactions, perform operations, check balance, and logout.

        Returns:
            None
        """
        pretty_print("Welcome to the Bank System!")
        self.load_data()
        while True:
            pretty_print("\n1. Login\n2. Exit\n")
            choice = input("Enter your choice: ")

            if choice == "1":
                user_type = input("Are you a customer or an admin? (_c_ustomer/_a_dmin): ").lower()
                if user_type == "customer" or user_type == "c":
                    login = input("Enter your login: ")
                    password = input("Enter your password: ")
                    self.login(login, password)
                elif user_type == "admin" or user_type == "a":
                    password = input("Enter admin password: ")
                    self.admin_login(password)
                else:
                    pretty_print("Invalid user type.")
            elif choice == "2":
                pretty_print("Exiting the Bank System. Goodbye!")
                break
            else:
                pretty_print("Invalid choice. Please try again.")

            if self.current_user:
                self.menu()

    def menu(self):
        """
        Displays the menu for logged-in users, allowing them to perform various operations.

        Returns:
            None
        """
        while True:
            print(f"\nCurrent user: {self.current_user}")
            if self.current_user == "admin":
                pretty_print("1. Create Customer\n2. Create Account\n3. View Transactions\n4. Perform Operations\n5. Delete Account\n6. Check Balance\n7. Logout\n")
                choice = input("Enter your choice: ")

                # Create Customer
                if choice == "1":
                    login = input("\nEnter customer login: ")
                    password = input("Enter customer password: ")
                    name = input("Enter customer name: ")
                    age = int(input("Enter customer age: "))
                    self.create_customer(name, age, login, password)

                # Create Account
                elif choice == "2":
                    pretty_print(f"This is avaible customers: {self.customers.keys()}")
                    login = input("Enter login for which user account will be created: ")
                    account_type = input("Enter account type (Savings/Checking): ")
                    self.create_account(self.customers[login].customer_id, account_type)

                # View Transactions
                elif choice == "3":
                    print("\n-----------------------------------")
                    print("Current Accounts: ")
                    for account in self.accounts:
                        if isinstance(self.accounts[account], SavingsAccount):
                            print(f"Account ID: {self.accounts[account].account_id}, Type: Savings")
                        elif isinstance(self.accounts[account], CheckingAccount):
                            print(f"Account ID: {self.accounts[account].account_id}, Type: Checking")
                    print("-----------------------------------")
                    account_id = input("\nEnter account ID to view transactions: ")
                    self.view_transactions(account_id)
                
                # Perform Operations
                elif choice == "4":
                    print("\n-----------------------------------")
                    print("Current Accounts: ")
                    for account in self.accounts:
                        if isinstance(self.accounts[account], SavingsAccount):
                            print(f"Account ID: {self.accounts[account].account_id}, Type: Savings")
                        elif isinstance(self.accounts[account], CheckingAccount):
                            print(f"Account ID: {self.accounts[account].account_id}, Type: Checking")
                    print("-----------------------------------")
                    account_id = input("\nEnter account ID to perform operations: ")
                    self.perform_operations(account_id)
                
                # Delete Account
                elif choice == "5":
                    print("\n-----------------------------------")
                    print("Current Accounts: ")
                    for account in self.accounts:
                        if isinstance(self.accounts[account], SavingsAccount):
                            print(f"Account ID: {self.accounts[account].account_id}, Type: Savings")
                        elif isinstance(self.accounts[account], CheckingAccount):
                            print(f"Account ID: {self.accounts[account].account_id}, Type: Checking")
                    print("-----------------------------------")
                    account_id = input("\nEnter account ID to delete account: ")
                    self.delete_account(account_id)
                
                # Check Balance
                elif choice == "6":
                    print("\n-----------------------------------")
                    print("Current Accounts: ")
                    for account in self.accounts:
                        if isinstance(self.accounts[account], SavingsAccount):
                            print(f"Account ID: {self.accounts[account].account_id}, Type: Savings")
                        elif isinstance(self.accounts[account], CheckingAccount):
                            print(f"Account ID: {self.accounts[account].account_id}, Type: Checking")
                    print("-----------------------------------")
                    account_id = input("\nEnter account ID to check balance: ")
                    if account_id not in self.accounts:
                        pretty_print("Account ID not found.")
                    else:
                        self.check_balance(account_id)
                
                # Exit
                elif choice == "7":
                    self.save_data()
                    self.logout()
                    break
                else:
                    pretty_print("Invalid choice. Please try again.")
            
            else:
                pretty_print("\n1. View Transactions\n2. Perform Operations\n3. Check Balance\n4. Logout\n")
                choice = input("Enter your choice: ")

                # View Transactions
                if choice == "1":
                    print("\n-----------------------------------")
                    print(f"Yours account:")
                    for account in self.accounts:
                        if self.accounts[account].customer_id == self.customers[self.current_user].customer_id:
                            if isinstance(self.accounts[account], SavingsAccount):
                                print(f"Account ID: {self.accounts[account].account_id}, Type: Savings")
                            elif isinstance(self.accounts[account], CheckingAccount):
                                print(f"Account ID: {self.accounts[account].account_id}, Type: Checking")
                    print("-----------------------------------")
                    account_id = input("Enter account ID to view transactions: ")
                    self.view_transactions(account_id)
                
                # Perform Operations
                elif choice == "2":
                    print("\n-----------------------------------")
                    print(f"Yours account:")
                    for account in self.accounts:
                        if self.accounts[account].customer_id == self.customers[self.current_user].customer_id:
                            if isinstance(self.accounts[account], SavingsAccount):
                                print(f"Account ID: {self.accounts[account].account_id}, Type: Savings")
                            elif isinstance(self.accounts[account], CheckingAccount):
                                print(f"Account ID: {self.accounts[account].account_id}, Type: Checking")
                    print("-----------------------------------")
                    account_id = input("Enter account ID to perform operations: ")
                    self.perform_operations(account_id)
                
                # Check Balance
                elif choice == "3":
                    print("\n-----------------------------------")
                    print(f"Yours account:")
                    for account in self.accounts:
                        if self.accounts[account].customer_id == self.customers[self.current_user].customer_id:
                            if isinstance(self.accounts[account], SavingsAccount):
                                print(f"Account ID: {self.accounts[account].account_id}, Type: Savings")
                            elif isinstance(self.accounts[account], CheckingAccount):
                                print(f"Account ID: {self.accounts[account].account_id}, Type: Checking")
                    print("-----------------------------------")
                    account_id = input("Enter account ID to check balance: ")
                    if account_id not in self.accounts:
                        pretty_print("Account ID not found.")
                    else:
                        self.check_balance(account_id)
                
                # Log Out
                elif choice == "4":
                    self.save_data()
                    self.logout()
                    break
                else:
                    pretty_print("Invalid choice. Please try again.")


if __name__ == "__main__":
    bank_system = BankSystem()
    bank_system.start()