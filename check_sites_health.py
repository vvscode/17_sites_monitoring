import requests
import ph4whois
import sys
from urllib.parse import urlparse
from prettytable import PrettyTable
import argparse
from datetime import datetime, timedelta


def load_urls4check(path):
    with open(path) as file:
        return [line.strip() for line in file.readlines()]


def is_server_respond_with_200(url, notes=[]):
    try:
        return requests.get(url).ok
    except requests.exceptions.ConnectionError:
        notes.append('Error with connection to server')
    except requests.exceptions.InvalidSchema:
        notes.append('Invalid schema')
    return False


def get_domain_expiration_date(domain_name):
    whois_info = ph4whois.whois(domain_name)
    return whois_info.expiration_date


def get_domain_from_url(url):
    return urlparse(url).hostname


def check_if_is_safety_prepaid(domain, notes=[]):
    prepaid_days_limit = 30
    critical_prepaid_date = datetime.now() + timedelta(days=prepaid_days_limit)
    try:
        expiration_date = get_domain_expiration_date(domain)
        return expiration_date < critical_prepaid_date
    except AttributeError:
        notes.append('Error with connection to whois server')
    except TypeError:
        notes.append('Error with connection to whois server')
    return False


def get_url_info(url):
    notes = []
    domain = get_domain_from_url(url)
    is_safety_prepaid = check_if_is_safety_prepaid(domain, notes=notes)
    is_status_200 = is_server_respond_with_200(url, notes=notes)

    return [url, domain, is_safety_prepaid, is_status_200, notes]


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
        [url, domain, is_safety_prepaid,
         is_status_200, notes] = get_url_info(url)
        table.add_row([
            url,
            domain,
            'Yes' if is_safety_prepaid else 'No',
            'Yes' if is_status_200 else 'No',
            '\n'.join(notes)
        ])

    print(table)
