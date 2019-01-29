# Sites Monitoring Utility

This script is a site monitoring helper. It cares about two things:

1. Check if your url responds with 200 status
1. Check if you domain prepaid at least for 1 month

Script takes a path to file with urls (1 per line) - that's required param. 
Reads urls and check information for every url.

Script uses external packages. You can install them with 

`pip3 install -r requirements.txt`

Example of usage:

```bash
$ python3 check_sites_health.py test.txt
List contains 5 domain(s)
+------------------------------------+-----------------------------+---------------------+------------+---------------------------------------+
| URL                                | Domain                      | Prepaid for a month | Status 200 | Notes                                 |
+------------------------------------+-----------------------------+---------------------+------------+---------------------------------------+
| http://ya.ru                       | ya.ru                       | No                  | Yes        | Error with connection to whois server |
| https://tut.by/about               | tut.by                      | No                  | No         | Error with connection to whois server |
| http://xxxx                        | xxxx                        | No                  | No         | Error with connection to whois server |
|                                    |                             |                     |            | Error with connection to server       |
| http://some_non-existing.domain.ru | some_non-existing.domain.ru | No                  | No         | Error with connection to whois server |
| xys://some-dummy-url.ru            | some-dummy-url.ru           | No                  | No         | Error with connection to whois server |
|                                    |                             |                     |            | Invalid schema                        |
+------------------------------------+-----------------------------+---------------------+------------+---------------------------------------+
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
