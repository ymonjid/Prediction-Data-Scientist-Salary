"""Extract median, min and max pay data from Glassdoor for a given set of job titles."""
from bs4 import BeautifulSoup
import requests
import sys


USER_AGENT = ("Mozilla/5.0 (Windows NT 6.1) "
              "AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/41.0.2228.0 Safari/537.36")


def perform_search(term):
    """Crawl Glassdoor to extract salary data."""
    length = len(term) + 3
    term = term.replace('(', '').replace(')', '').replace(' ', '-').lower()
    glassdoor = "https://www.glassdoor.com"
    slug = "{gd}/Salaries/us-{term}-salary-SRCH_IL.0,2_IN1_KO3,{l}.htm"
    url = slug.format(gd=glassdoor, term=term, l=length)
    headers = {'User-Agent': USER_AGENT}
    response = requests.get(url, headers=headers, allow_redirects=False)
    return response


def parse_data(response):
    """Parse out the response HTML."""
    soup = BeautifulSoup(response.content, "lxml")
    salary = soup.find('div', {'class': 'salaryRow'})
    if not salary:
        return False
    pay_check = salary.find('div', {'id': 'MeanPay_N'})
    if not pay_check:
        return False
    median = str(salary.find('div', {'id': 'MeanPay_N'}).text.rstrip().lstrip())
    min_pay = str(salary.find('div', {'class': 'minPay'}).text.rstrip().lstrip())
    max_pay = str(salary.find('div', {'class': 'maxPay'}).text.rstrip().lstrip())
    return (median, min_pay.replace('k', ',000'), max_pay.replace('k', ',000'))


def main():
    """Unleash the machines."""
    if len(sys.argv) < 2:
        print("Usage: python glassdoor-salary-scraper.py /file/path/jobs.txt")
        sys.exit(1)
    f = open('position-salary-data.txt', 'a')
    titles = [x.strip() for x in open(sys.argv[1], 'r').readlines()]
    for title in titles:
        response = perform_search(title)
        data = parse_data(response)
        if not data:
            row = "|".join([title, '', '', ''])
        else:
            median, mi, ma = data
            row = "|".join([title, median, mi, ma])
        f.write(row + "\n")
        print(row)
    f.close()

if __name__ == "__main__":
    main()