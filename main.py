from date import Date
from financier import Financier


def main():

    def format_currency(amount):
        neg_sign = lambda x: '-' if x < 0 else ''
        return f'{neg_sign(amount)}${abs(amount):.02f}'

    financier = Financier('subscriptions.csv',
                          'plaid_credentials.json',
                          'bank_credentials.json')
    debt = financier.calculate_debt()
    payday = Date.today().next_payday()
    balance = financier.get_balance()
    msg = '\n'.join([
        f'BALANCE = {format_currency(balance)}',
        f'DEBT = {format_currency(debt)}',
        f'SPEND = {format_currency(balance - debt)}',
        f'PAYDAY = {repr(payday)}',
    ])
    with open('results', 'r') as f:
        f.write(msg)


if __name__ == '__main__':
    main()
