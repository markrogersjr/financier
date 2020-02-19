import os
from argparse import ArgumentParser
from date import Date
from financier import Financier


def main():

    parser = ArgumentParser()
    parser.add_argument('--subscriptions_filename')
    parser.add_argument('--plaid_credentials_filename')
    parser.add_argument('--bank_credentials_filename')
    args = parser.parse_args()

    financier = Financier(args.subscriptions_filename,
                          args.plaid_credentials_filename,
                          args.bank_credentials_filename)
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
