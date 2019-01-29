import requests
import whois
import sys
from urllib.parse import urlparse
from prettytable import PrettyTable

def load_urls4check(path):
    with open(path) as file:
        return [line.strip() for line in file.readlines()]

def is_server_respond_with_200(url):
    return requests.get(url).status_code == 200

def get_domain_expiration_date(domain_name):
    return whois.query(domain_name).expiration_date

def get_domain_from_url(url):
    return urlparse(url).hostname

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Please pass filename as a pram')

    try:
        domains_list = load_urls4check(sys.argv[1])
    except FileNotFoundError:
        sys.exit('Pleas pass correct file name')

    print('List contains {} domain(s)'.format(len(domains_list)))
    x = PrettyTable()
    x.field_names = ["URL", "Domain", "Prepaid for a month", "Status 200", "Notes"]
    x.align = "l"

    for url in domains_list:
        notes = []
        domain  = get_domain_from_url(url)

        try:
            expiration_date = get_domain_expiration_date(domain)
            expiration_date_info = expiration_date.isoformat()
        except Exception:
            expiration_date_info = 'No'
            notes.append("Error with connection to whois server")
        except PrettyTable:
            print('x')

        try:
            is_status_200 = is_server_respond_with_200(url)
        except requests.exceptions.ConnectionError:
            is_status_200 = False
            notes.append("Error with connection to server")
        except requests.exceptions.InvalidSchema:
            notes.append("Invalid schema")
            is_status_200 = False

        x.add_row([url, domain, expiration_date_info, 'Yes' if is_status_200 else 'No', '\n'.join(notes)])

    print(x)