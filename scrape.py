# coding: utf-8
import datetime
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv

FROM_DATE = '2017-06-01'
TO_DATE = '2017-06-30'
URL_ALL_TRANSACTIONS = 'https://www.bitstock.com/cs/trades?from={}&to={}&user=-1&account=-1'.format(FROM_DATE, TO_DATE)

response = requests.get(URL_ALL_TRANSACTIONS)
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find_all('table')[0]
rows = table.find_all('tr')

raw_transactions = []

for row in rows:
    tds = row.find_all('td')
    transaction = [x.text.strip() for x in tds]
    raw_transactions.append(transaction)
    
# First row is empty, drop it
raw_transactions = raw_transactions[1:]


def erase_columns(t):
    """
    Only keeps the id, timestamp, unit price and amout of the transaction.
    """
    indexes = [
        0,  # id
        2,  # timestamp
        3,  # price per BTC
        4,  # amount
    ]
    return [t[x] for x in indexes]


def string_to_date(t):
    """
    transforms date string inside the transaction into datetime object.
    """
    t[1] = datetime.strptime(t[1], '%d.%m.%y, %H:%M')
    return t


def string_to_float(t):
    """
    Converts price and amount from string to floating
    point number.
    """
    indexes = [2,3]
    for i in indexes:
        t[i] = float(t[i].replace(' ', '').replace(',', '.'))
    return t


def clean_transactions(transactions):
    transformations = [erase_columns, string_to_date, string_to_float]
    for transform in transformations:
        transactions = [transform(x) for x in transactions]
    return transactions


cleaned = clean_transactions(raw_transactions)
cleaned.sort(key=lambda x: x[1])  # Sort chronologically.


# Write out as csv file.
with open('transactions.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(cleaned)




