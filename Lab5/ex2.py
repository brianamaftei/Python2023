from datetime import datetime, timedelta
import sys


class Account:
    def __init__(self, balance, open_date, expire_date=None):
        self.balance = balance
        self.open_date = open_date
        if expire_date is None:
            self.expire_date = open_date + timedelta(days=365)
        self.history = []

    def transaction(func):
        def wrapper(self, amount):
            self.history.append([f"{func.__name__} : {amount}, date:{datetime.now().date()}"])
            return func(self, amount)

        return wrapper

    @transaction
    def deposit(self, amount):
        self.balance += amount

    @transaction
    def withdraw(self, amount):
        if amount > self.balance:
            raise Exception(
                f"Not enough money in the {type(self).__name__} to withdraw {amount}. Balance: {self.balance}")
        self.balance -= amount

    def __add__(self, amount):
        if type(amount) not in (int, float):
            raise TypeError("The value must be an int, float")
        if amount < 0:
            raise Exception("Amount withdraw must be greater or equal than 0")
        return Account(self.balance + amount, self.open_date)

    def __sub__(self, amount):
        if type(amount) not in (int, float):
            raise TypeError("The value must be an int, float")
        if amount < 0:
            raise Exception("Amount withdraw must be greater or equal than 0")
        return Account(self.balance - amount, self.open_date)

    def __setattr__(self, key, value):
        try:
            if type(value) is list:
                if key != "history":
                    raise TypeError("The value must be an int, float 1")

            elif type(value) is datetime:
                if key not in ("open_date", "last_interest_date", "expire_date", "due_time"):
                    raise TypeError("The value must be an int, float 4")

            elif type(value) not in (int, float):
                raise TypeError("The value must be an int, float")

            object.__setattr__(self, key, value)

        except TypeError as e:
            print(e)
            sys.exit()

    def __str__(self):
        result = f"{type(self).__name__}'s information: \n"
        all_attributes = list(vars(self).items())
        for attribute in all_attributes:
            result += f"{attribute[0]} is {attribute[1]} \n"
        return result

    def __enter__(self):
        try:
            if self.expire_date < datetime.now():
                raise Exception("Account has expired")
            return self
        except Exception as e:
            print(e)
        sys.exit()


class CheckingAccount(Account):
    def __init__(self, balance, open_date):
        Account.__init__(self, balance, open_date)


class SavingAccount(Account):
    def __init__(self, balance, interest_rate, open_date, last_interest_date=None):
        Account.__init__(self, balance, open_date)
        self.interest_rate = interest_rate
        if last_interest_date is None:
            self.last_interest_date = open_date
        else:
            self.last_interest_date = last_interest_date

    def calculate_interest(self):
        return self.balance * self.interest_rate

    def __exit__(self, exc_type, exc_val, exc_tb):
        if datetime.now() - self.last_interest_date >= timedelta(days=1) and self.balance > 0:
            self.balance += self.calculate_interest()
            self.last_interest_date = datetime.now()
            print("New balance with interest added: ", self.balance)


class DepositAccount(SavingAccount):
    def __init__(self, balance, interest_rate, open_date, due_time, last_interest_date=None):
        SavingAccount.__init__(self, balance, interest_rate, open_date, last_interest_date)
        self.due_time = due_time
        self.gathered_money = 0

    def calculate_interest(self):
        return self.balance * self.interest_rate / (self.due_time - self.open_date).days * (
                datetime.now() - self.last_interest_date).days

    def transaction(func):
        def wrapper(self, amount):
            self.history.append([f"{func.__name__} : {amount}, date:{datetime.now().date()}"])
            return func(self, amount)

        return wrapper

    @transaction
    def withdraw(self, amount):
        if datetime.now() < self.due_time:
            self.balance = self.balance - self.gathered_money - amount
            self.gathered_money = 0


account = Account(100, open_date=datetime.now())
print(account)

saving_account = SavingAccount(100, 0.1, open_date=datetime(2023, 11, 11))
with saving_account:
    saving_account.deposit(100)
    saving_account.withdraw(50)
print(saving_account)

deposit_account = DepositAccount(100, 0.6, open_date=datetime(2023, 11, 11), due_time=datetime(2024, 11, 16))
with deposit_account:
    deposit_account.deposit(100)
    deposit_account.withdraw(10)
print(deposit_account)
