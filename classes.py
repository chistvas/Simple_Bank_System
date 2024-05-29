class Customer:
    """
    Represents a bank customer with attributes such as customer ID, name, age, login, and password.

    Attributes:
        customer_id (str): The unique identifier for the customer.
        name (str): The name of the customer.
        age (int): The age of the customer.
        login (str): The login ID for the customer.
        password (str): The password for the customer's account.
    """
    def __init__(self, customer_id: str, name: str, age: int, login: str, password: str):
        """
        Initializes a Customer object with provided attributes.

        Args:
            customer_id (str): The unique identifier for the customer.
            name (str): The name of the customer.
            age (int): The age of the customer.
            login (str): The login ID for the customer.
            password (str): The password for the customer's account.
        """
        self.customer_id = customer_id
        self.name = name
        self.age = age
        self.login = login
        self.password = password

    def __str__(self):
        """
        Returns a string representation of the Customer object.

        Returns:
            str: A formatted string containing customer information.
        """
        return f"Customer ID: {self.customer_id}, Name: {self.name}, Age: {self.age}, Login: {self.login}"
    
class Account:
    """
    Represents a general account with attributes including account ID, customer ID, and balance.

    Attributes:
        account_id (str): The unique identifier for the account.
        customer_id (str): The customer ID associated with the account.
        balance (float): The current balance in the account.
    """
    def __init__(self, account_id: str, customer_id: str, balance: float=0):
        """
        Initializes an Account object with provided attributes.

        Args:
            account_id (str): The unique identifier for the account.
            customer_id (str): The customer ID associated with the account.
            balance (float, optional): The initial balance in the account. Defaults to 0.
        """
        self.account_id = account_id
        self.customer_id = customer_id
        self.balance = balance

    def deposit(self, amount: float):
        """
        Deposits a specified amount into the account.

        Args:
            amount (float): The amount to deposit into the account.

        Returns:
            bool: True if the deposit is successful, False otherwise.
        """
        self.balance += amount
        return True

    def withdrawal(self, amount: float):
        """
        Withdraws a specified amount from the account.

        Args:
            amount (float): The amount to withdraw from the account.

        Returns:
            bool: True if the withdrawal is successful, False otherwise.
        """
        self.balance -= amount
        return True
    
    def show_balance(self):
        """
        Displays the current balance of the account.
        """
        print(f"Account ID: {self.account_id}")
        print(f"Customer ID: {self.customer_id}")
        print(f"Current Balance: {self.balance}")
        if self.balance < 0:
            print("Account Status: Overdrawn")
        else:
            print("Account Status: Active")

    def __str__(self):
        """
        Returns a string representation of the Account object.

        Returns:
            str: A formatted string containing account information.
        """
        return f"Account ID: {self.account_id}, Customer ID: {self.customer_id}, Balance: {self.balance}"

class SavingsAccount(Account):
    """
    Represents a savings account, inheriting from the Account class.

    Attributes:
        monthly_withdrawals (int): The number of monthly withdrawals allowed.
    """
    def __init__(self, account_id: str, customer_id: str, balance: float=0, monthly_withdrawals:int=1):
        """
        Initializes a SavingsAccount object with provided attributes.

        Args:
            account_id (str): The unique identifier for the account.
            customer_id (str): The customer ID associated with the account.
            balance (float, optional): The initial balance in the account. Defaults to 0.
            monthly_withdrawals (int, optional): The number of monthly withdrawals allowed. Defaults to 1.
        """
        super().__init__(account_id, customer_id, balance)
        self.monthly_withdrawals = monthly_withdrawals
    
    def withdrawal(self, amount: float):
        """
        Withdraws a specified amount from the savings account, considering monthly withdrawal limit.

        Args:
            amount (float): The amount to withdraw from the account.

        Returns:
            bool: True if the withdrawal is successful, False otherwise.
        """
        if self.monthly_withdrawals > 0:
            self.balance -= amount
            self.monthly_withdrawals -= 1
            return True
        else:
            print("Monthly withdrawal limit exceeded.")
            return False
    
    def transfer(self, amount: float, recipient_account: Account):
        """
        Transfers a specified amount from the savings account to another account.

        Args:
            amount (float): The amount to transfer.
            recipient_account (Account): The recipient account to transfer the amount to.

        Returns:
            bool: True if the transfer is successful, False otherwise.
        """
        if self.monthly_withdrawals > 0:
            self.balance -= amount
            recipient_account.deposit(amount)
            self.monthly_withdrawals -= 1
            return True
        else:
            print("Monthly tranfer limit exceeded.")
            return False

    def __str__(self):
        """
        Returns a string representation of the SavingsAccount object.

        Returns:
            str: A formatted string containing account information.
        """
        return super().__str__() + f", Monthly Withdrawals Left: {self.monthly_withdrawals}"

class CheckingAccount(Account):
    """
    Represents a checking account, inheriting from the Account class.

    Attributes:
        credit_limit (float): The credit limit for the checking account.
    """
    def __init__(self, account_id: str, customer_id: str, balance: float=0, credit_limit: float=0):
        """
        Initializes a CheckingAccount object with provided attributes.

        Args:
            account_id (str): The unique identifier for the account.
            customer_id (str): The customer ID associated with the account.
            balance (float, optional): The initial balance in the account. Defaults to 0.
            credit_limit (float, optional): The credit limit for the checking account. Defaults to 0.
        """
        super().__init__(account_id, customer_id, balance)
        self.credit_limit = credit_limit
    
    def withdrawal(self, amount: float):
        """
        Withdraws a specified amount from the checking account, considering credit limit.

        Args:
            amount (float): The amount to withdraw from the account.

        Returns:
            bool: True if the withdrawal is successful, False otherwise.
        """
        if self.balance + self.credit_limit >= amount:
            self.balance -= amount
            return True
        else:
            print("Not enough funds to withdrawal.")
            return False

    def transfer(self, amount: float, recipient_account: Account):
        """
        Transfers a specified amount from the checking account to another account.

        Args:
            amount (float): The amount to transfer.
            recipient_account (Account): The recipient account to transfer the amount to.

        Returns:
            bool: True if the transfer is successful, False otherwise.
        """
        if self.balance + self.credit_limit >= amount:
            self.balance -= amount
            recipient_account.deposit(amount)
            return True
        else:
            print("Not enough funds to transfer.")
            return False
        
    def __str__(self):
        """
        Returns a string representation of the CheckingAccount object.

        Returns:
            str: A formatted string containing account information.
        """
        return super().__str__() + f", Credit Limit: {self.credit_limit}"

def pretty_print(string: str) -> str:
    """
    Formats a string with a delimiter for better readability.

    Args:
        string (str): The string to be formatted.

    Returns:
        str: The formatted string with delimiters.

    Example:
        >>> pretty_print("Hello, world!")
        -----------------------------------
        Hello, world!
        -----------------------------------
    """
    ret = f"\n-----------------------------------\n{string}\n-----------------------------------"
    return print(ret)