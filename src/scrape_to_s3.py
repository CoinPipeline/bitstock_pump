import requests
from datetime import datetime
import tempfile
import boto3


def get_transactions():
    """
    Requests and returns raw html transaction data in
    fixed time period.
    :return: Response text
    """
    FROM_DATE = '2017-06-01'
    TO_DATE = '2017-06-30'
    URL_ALL_TRANSACTIONS = 'https://www.bitstock.com/cs/trades?from={}&to={}&user=-1&account=-1'.format(FROM_DATE, TO_DATE)
    response = requests.get(URL_ALL_TRANSACTIONS)
    return response.text


def scrape_and_write_raw(event, context):
    """
    Writes transaction raw html to timestamped s3 bucket.
    :param event:
    :param context:
    :return:
    """
    BUCKET_NAME = 'bitstock-transactions'
    timestamp = datetime.utcnow().isoformat().replace('.', '_')
    filename = 'bitstock_transactions_raw_{}.txt'.format(timestamp)
    tmpfile = tempfile.NamedTemporaryFile(delete=False)
    tmpfile.write(bytes(get_transactions(), 'UTF-8'))
    tmpfilename = tmpfile.name
    tmpfile.close()
    s3 = boto3.client('s3')
    s3.upload_file(tmpfilename, BUCKET_NAME, filename)
