import json
from BankAccount import BankAccount


class Atm:

    def __init__(self, account_data='accounts.json'):
        self.data = None
        self.account_data = account_data
        self.accounts = self.load_data()

    def load_data(self):
        try:
            with open(self.account_data, 'r') as data:
                return json.load(data)
        except FileNotFoundError:
            return {}

    def saveData(self):
        with open(self.account_data, 'w') as data:
            json.dump(self.account_data, data)

    def createAccount(self, acc_number, acc_holder, acc_pin):
        if acc_number in self.accounts:
            print('This account has exists')
            return False
        self.accounts[acc_number] = {
            'holder': acc_holder,
            'pin': acc_pin,
            'balance': 0
        }
        self.saveData()
        print(f"Account's number: [{acc_number}] has been created.")
        self.atm_menu()
        return True

    def authenticate(self, acc_number, acc_pin):
        if acc_number not in self.accounts:
            print(f"Account's number [{acc_number}] doesn't exists.")
            return False
        if self.accounts[acc_number]['pin'] != acc_pin:
            print(f'Password not correct.')
            return False
        return BankAccount(acc_number, self.accounts[acc_number]['holder'], acc_pin,
                           self.accounts[acc_number]['balance'])

    def management_menu(self, account):
        while True:
            print('Welcome to Management Menu'
                  '\nChoose choice here:'
                  '\n1.Deposit'
                  '\n2.Withdraw'
                  '\n3.Close Bank Account'
                  '\n4.Exit')
            choice = int(input('Enter your choice: '))
            if choice == 1:
                amount = float(input('Enter amount to deposit: '))
                if amount <= 0:
                    print('Please enter positive number.')
                    return
                account.deposit(amount)
                self.accounts[self.data['acc_number']]['balance'] = account.getBalance()
                self.saveData()
            elif choice == 2:
                amount = float(input('Enter amount to withdraw: '))
                if amount < account.getBalance():
                    print('Insufficient balance to withdraw.')
                    return
                account.withdraw(amount)
                self.accounts[self.data['acc_number']]['balance'] = account.getBalance()
                self.saveData()
            elif choice == 3:
                pass
            elif choice == 4:
                print('Thank you for using ATM.')
                break

    def atm_menu(self):
        while True:
            print('Welcome to ATM Menu'
                  '\nChoose choice here:'
                  '\n1.Create Bank Account'
                  '\n2.Login'
                  '\n3.Exit')
            choice = int(input('Enter your choice: '))
            if choice == 1:
                acc_holder = input('Enter your name: ')
                acc_pin = input('Enter your pin code (6 digits): ')
                if len(acc_pin) != 6:
                    print('Pin code must be 6 digits')
                    return
                self.createAccount(342531, acc_holder, acc_pin)
            elif choice == 2:
                acc_holder = input('Enter your name: ')
                acc_pin = input('Enter your pin code (6 digits): ')
                authed = self.authenticate(acc_holder, acc_pin)
                if authed:
                    self.management_menu(authed)
            elif choice == 3:
                print()
