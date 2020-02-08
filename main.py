from date import Date
from financier import Financier


def main():
    financier = Financier('subscriptions.csv',
                          'plaid_credentials.json',
                          'bank_credentials.json')
    debt = financier.calculate_debt()
    payday = Date.today().next_payday()
    print(f'You must keep at least ${debt:.02f} in your checking account until {payday}.')


if __name__ == '__main__':
    main()
