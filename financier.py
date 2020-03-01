import json
import pandas as pd
from date import Date
from plaid import Client


class Financier:

    @classmethod
    def is_match(cls, subscription, transaction):
        return all([
            subscription.alias.lower() in transaction.name.lower(),
            0 <= transaction.date - subscription.date < 15,
            abs(subscription.amount - transaction.amount) < 5,
        ])

    class Subscription:
    
        def __init__(self, name, amount, date, alias):
            self.name = name
            self.amount = amount
            self.date = date
            self.alias = alias

        def __repr__(self):
            return f'Subscription({self.name}(={self.alias}), ${self.amount:.02f} on {self.date}'

        def matches(self, transaction):
            return Financier.is_match(self, transaction)

    class Transaction:

        def __init__(self, name, amount, date):
            self.name = name
            self.amount = amount
            self.date = date

        def __repr__(self):
            return f'Transaction({self.name}, ${self.amount:.02f} on {self.date}'

        def matches(self, subscription):
            return Financier.is_match(subscription, self)

        def __eq__(self, other):
            return all([
                isinstance(other, Financier.Transaction),
                self.name == other.name,
                self.amount == other.amount,
                self.date == other.date,
            ])

    def __init__(self,
                 subscriptions_table_filename,
                 plaid_credentials_filename,
                 bank_credentials_filename):
        self.subscriptions_table = pd.read_csv(subscriptions_table_filename)
        with open(plaid_credentials_filename, 'r') as f:
            self.client = Client(**json.load(f), environment='development')
        with open(bank_credentials_filename, 'r') as f:
            self.access_token = json.load(f)['access_token']
        self.client.Auth.get(self.access_token)

    def get_subscriptions(self):
        today = Date.today()
        last_day = Date.last_of_month().day
        next_payday = today.next_payday()
        prev_payday = today.prev_payday()
        dates = []
        for i, day in enumerate(self.subscriptions_table.Day):
            if day >= next_payday.day:
                year, month = next_payday.prevmonth()
            else:
                year, month = next_payday.year, next_payday.month
            day = min(day, Date.last_of_month(year, month).day)
            date = Date(year, month, day)
            dates.append(date)
        subscriptions = []
        for i, name, amount, day, alias in self.subscriptions_table.to_records():
            subscription = self.Subscription(name, amount, dates[i], alias)
            subscriptions.append(subscription)
        return subscriptions

    def get_balance(self):
        today = Date.today()
        response = self.client.Transactions.get(self.access_token,
                                                str(today),
                                                str(today))
        balance = 0
        for account in response['accounts']:
            if account['type'] == 'depository':
                balance += account['balances']['available']
        return balance

    def get_transactions(self, start_date, end_date):

        def process_batch(start_date, end_date):
            response = self.client.Transactions.get(self.access_token,
                                                    str(start_date),
                                                    str(end_date),
                                                    count=500)
            for new_dict in response['transactions']:
                new_transaction = self.Transaction(new_dict['name'],
                                                   new_dict['amount'],
                                                   Date(new_dict['date']))
                if not transactions:
                    transactions.append(new_transaction)
                else:
                    for i in range(len(transactions)):
                        transaction = transactions[-1 - i]
                        if transaction.date != new_transaction.date:
                            transactions.append(new_transaction)
                            break
                        elif transaction == new_transaction:
                            break
                        else:
                            continue
                
        transactions = []
        while not transactions or transactions[-1].date > start_date:
            if transactions:
                end_date = transactions[-1].date
            process_batch(start_date, end_date)
        process_batch(start_date, start_date)
        return transactions

    @classmethod
    def format_currency(cls, amount, digits=4):
        neg = '-' if amount < 0 else ''
        return f'{neg}${abs(amount):.02f}'.rjust(digits + len('-$.00'))

    def get_remaining_subscriptions(self):
        today = Date.today()
        prev_payday = today.prev_payday()
        subscriptions = self.get_subscriptions()
        subscriptions = [s for s in subscriptions if s.date >= prev_payday]
        transactions = self.get_transactions(prev_payday, today)
        remaining_subscriptions = []
        for subscription in subscriptions:
            has_match = False
            for transaction in transactions:
                if subscription.matches(transaction):
                    has_match = True
                    break
            if not has_match:
                remaining_subscriptions.append(subscription)
        return remaining_subscriptions

    def calculate_debt(self):
        return sum(sub.amount for sub in self.get_remaining_subscriptions())
