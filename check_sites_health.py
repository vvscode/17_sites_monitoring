import requests
import whois
import sys
from urllib.parse import urlparse
from prettytable import PrettyTable
import argparse
from datetime import datetime, timedelta
import collections

url_info = collections.namedtuple(
    'url_info', ['url', 'domain', 'is_prepaid', 'is_status_200', 'notes'])


def load_urls4check(path):
    with open(path) as file:
        return [line.strip() for line in file.readlines()]


def validate_response_status(url):
    notes = []
    try:
        response = requests.get(url)
        if response.ok:
            return []
        return ['Status code is {}'.format(requests.get(url).ok)]
    except requests.exceptions.ConnectionError:
        return ['Error with connection to server']
    except requests.exceptions.InvalidSchema:
        return ['Invalid schema']

def get_domain_expiration_date(domain_name):
    whois_info = whois.whois(domain_name)
    return whois_info.expiration_date


def get_domain_from_url(url):
    return urlparse(url).hostname


def validate_prepayment(domain):
    prepaid_days_limit = 30
    critical_prepaid_date = datetime.now() + timedelta(days=prepaid_days_limit)
    try:
        expiration_date = get_domain_expiration_date(domain)
        if not expiration_date:
            return ['Expiration date not available']
        if expiration_date < critical_prepaid_date:
            return []
        return ["Prepaid till {}".format(expiration_date.isoformat())]
    except ConnectionRefusedError:
        return ['Error with connection to whois server']


def get_url_info(url):
    notes = []
    domain = get_domain_from_url(url)

    response_validation_errors = validate_response_status(url)
    prepaid_validation_errors = validate_prepayment(domain)

    notes.extend(response_validation_errors)
    notes.extend(prepaid_validation_errors)

    return url_info(
        url=url,
        domain=domain,
        is_prepaid=not len(prepaid_validation_errors),
        is_status_200=not len(response_validation_errors),
        notes=notes
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sites monitor')
    parser.add_argument('file_path', help='Path to file with urls')
    args = parser.parse_args()

    try:
        domains_list = load_urls4check(args.file_path)
    except FileNotFoundError:
        sys.exit('Pleas pass correct file name')

    print('List contains {} domain(s)'.format(len(domains_list)))
    table = PrettyTable()
    table.field_names = ['URL', 'Domain',
                         'Prepaid for a month', 'Status 200', 'Notes']
    table.align = 'l'

    for url in domains_list:
        info = get_url_info(url)
        table.add_row([
            info.url,
            info.domain,
            'Yes' if info.is_prepaid else 'No',
            'Yes' if info.is_status_200 else 'No',
            '\n'.join(info.notes)
        ])

    print(table)
