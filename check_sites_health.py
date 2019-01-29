import requests
import whois
import sys
from urllib.parse import urlparse
from prettytable import PrettyTable
import argparse
from datetime import datetime, timedelta
import collections

url_info = collections.namedtuple(
    "url_info", ["url", "domain", "is_prepaid", "is_status_200", "notes"])


def load_urls4check(path):
    with open(path) as file:
        return [line.strip() for line in file.readlines()]


def is_status_code_equal(url, status_code):
    try:
        response = requests.get(url)
        return response.status_code == status_code, None

    except requests.exceptions.ConnectionError:
        return False, "Error with connection to server"
    except requests.exceptions.InvalidSchema:
        return False, "Invalid schema"


def get_domain_expiration_date(domain_name):
    whois_info = whois.whois(domain_name)
    expiration_date = whois_info.expiration_date
    expiration_date = expiration_date[0] if isinstance(expiration_date, list) else expiration_date
    return expiration_date


def get_domain_from_url(url):
    return urlparse(url).hostname


def is_domain_prepaid(domain, prepaid_days_limit=7):
    critical_prepaid_date = datetime.now() + timedelta(days=prepaid_days_limit)
    try:
        expiration_date = get_domain_expiration_date(domain)
        if not expiration_date:
            return False, "Expiration date not available"
        if expiration_date > critical_prepaid_date:
            return True, None
        return False, "Prepaid till {}".format(expiration_date)
    except ConnectionRefusedError:
        return False, "Error with connection to whois server"


def get_url_info(url):
    notes = []
    domain = get_domain_from_url(url)
    prepaid_period = 30
    expected_status_code = 200

    is_status_200, response_validation_error = is_status_code_equal(url, expected_status_code)
    if response_validation_error:
        notes.append(response_validation_error)

    is_prepaid, prepaid_validation_error = is_domain_prepaid(domain, prepaid_period)

    if prepaid_validation_error:
        notes.append(prepaid_validation_error)

    return url_info(
        url=url,
        domain=domain,
        is_prepaid=is_prepaid,
        is_status_200=is_status_200,
        notes=notes
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sites monitor")
    parser.add_argument("file_path", help="Path to file with urls")
    args = parser.parse_args()

    try:
        domains_list = load_urls4check(args.file_path)
    except FileNotFoundError:
        sys.exit("Pleas pass correct file name")

    print("List contains {} domain(s)".format(len(domains_list)))
    table = PrettyTable()
    table.field_names = ["URL", "Domain",
                         "Prepaid for a month", "Status 200", "Notes"]
    table.align = "l"

    for url in domains_list:
        site_info = get_url_info(url)
        table.add_row([
            site_info.url,
            site_info.domain,
            "Yes" if site_info.is_prepaid else "No",
            "Yes" if site_info.is_status_200 else "No",
            "\n".join(site_info.notes)
        ])

    print(table)
