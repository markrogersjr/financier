import os
from date import Date
from financier import Financier


def main():

    financier = Financier('subscriptions.csv',
                          'plaid_credentials.json',
                          'bank_credentials.json')
    debt = financier.calculate_debt()
    payday = Date.today().next_payday()
    balance = financier.get_balance()
    msg = '\n'.join([
        f'BALANCE = {Financier.format_currency(balance)}',
        f'DEBT = {Financier.format_currency(debt)}',
        f'SPEND = {Financier.format_currency(balance - debt)}',
        f'PAYDAY = {repr(payday)}',
    ])
    print(msg)
    with open('results', 'w') as f:
        f.write(msg)


if __name__ == '__main__':
    main()
