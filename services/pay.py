import requests
from environs import Env

from settings import TOKEN, JAR_ID


def get_ranged_statements(time_from: str | int, time_to: str | int = ''):
    headers = {
        'X-Token': TOKEN
    }
    return requests.get(f'https://api.monobank.ua/personal/statement/{JAR_ID}/{time_from}/{time_to}',
                        headers=headers).json()


def filter_only_plus_statements(statements: list[dict]):
    return list(filter(lambda statement: statement['amount'] > 0, statements))


def get_ony_plus_filtered_ranged_statements(time_from: str | int, time_to: str | int = ''):
    ranged_statements = get_ranged_statements(time_from, time_to)
    return filter_only_plus_statements(ranged_statements)


if __name__ == '__main__':
    response = get_ranged_statements(1671267430, 1671270088)
    filtered = filter_only_plus_statements(response)
    print(filtered)
