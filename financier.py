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
        next_payday = today.next_payday()
        prev_payday = today.prev_payday()
        dates = []
        for i, day in enumerate(self.subscriptions_table.Day):
            if day >= next_payday.day:
                year, month = next_payday.prevmonth()
                date = Date(year, month, day)
                dates.append(date)
            else:
                print(next_payday.year, next_payday.month, day)
                date = Date(next_payday.year, next_payday.month, day)
                dates.append(date)
        subscriptions = []
        for i, name, alias in self.subscriptions_table.to_records():
            subscription = self.Subscription(name, amount, dates[i], alias)
            subscriptions.append(subscription)
        return subscriptions

    def get_transactions(self, start_date, end_date):
        transactions = []
        while not transactions or Date(transactions[-1]['date']) > start_date:
            if transactions:
                end_date = Date(transactions[-1]['date'])
            response = self.client.Transactions.get(self.access_token, str(start_date), str(end_date))
            transactions.extend(response['transactions'])
        response = self.client.Transactions.get(self.access_token, str(start_date), str(start_date))
        transactions.extend(response['transactions'])
        transactions_set = set(map(json.dumps, transactions))
        transaction_dicts = sorted(map(json.loads, transactions_set), key=lambda t: -t['date'])
        transactions = []
        for t in transaction_dicts:
            transaction = self.Transaction(t['name'], t['amount'], Date(t['date']))
            transactions.append(transaction)
        return transactions

    def calculate_debt(self):
        today = Date.today()
        prev_payday = today.prev_payday()
        subscriptions = self.recurring_payments.get_subscriptions()
        subscriptions = [s for s in subscriptions if s.date >= prev_payday]
        transactions = self.bank_client.get_transactions(prev_payday, today)
        remaining_subscriptions = []
        for i, subscription in enumerate(subscriptions):
            has_match = False
            for transaction in transactions:
                if subscription.matches(transaction):
                    has_match = True
                    break
            if not has_match:
                remaining_subscriptions.append(i)
        return sum(subscriptions[i].amount for i in remaining_subscriptions)
