import os
from argparse import ArgumentParser
from date import Date
from financier import Financier


def main():

    parser = ArgumentParser()
    parser.add_argument('--subscriptions_filename')
    parser.add_argument('--plaid_credentials_filename')
    parser.add_argument('--bank_credentials_filename')
    parser.add_argument('--from_email')
    parser.add_argument('--to_email')
    args = parser.parse_args()

    financier = Financier(args.subscriptions_filename,
                          args.plaid_credentials_filename,
                          args.bank_credentials_filename)
    debt = financier.calculate_debt()
    payday = Date.today().next_payday()
    balance = financier.get_balance()
    header = [
        f'From: {args.from_email}',
        f'To: {args.to_email}',
        f'Subject: Personal Finance Report',
        f'Content-Type: text/html; charset=utf-8',
        f'<!DOCTYPE html>'
    ]
    header = '\n'.join(header)
    body = [
        f'BALANCE = {Financier.format_currency(balance)}',
        f'DEBT = {Financier.format_currency(debt)}',
        f'SPEND = {Financier.format_currency(balance - debt)}',
        f'PAYDAY = {repr(payday)}',
    ]
    remaining_subscriptions = financier.get_remaining_subscriptions()
    if remaining_subscriptions:
        body.extend(['', 'REMAINING SUBSCRIPTIONS'])
        table = ['<table style="font-size:10px;font-weight:normal">']
        for sub in remaining_subscriptions:
            amount = Financier.format_currency(sub.amount).strip()
            date = f'{sub.date.month}/{sub.date.day}'
            row = [f'{sub.name}', f'{amount}', f'{date}']
            row = ''.join(f'<th>{c}</th>' for c in row)
            table.append('<tr>' + row + '</tr>\n')
        table.append('</table>')
        body.append(''.join(table))
    body = '<br>\n'.join(body)
    body = '<html><body>' + body + '</body></html>'
    msg = header + body
    with open('results', 'w') as f:
        f.write(msg)


if __name__ == '__main__':
    main()
