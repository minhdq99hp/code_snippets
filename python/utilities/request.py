'''
Utility functions for working with requests

Author: minhdq99hp@gmail.com
'''
import requests
from time import sleep

class RetryLimitExceededException(Exception):
    pass

def send_request(url, data={}, method='post', headers={}, timeout=60, max_retry=3, delay=0, silent=True, exc_msg=''):
    '''
    Send HTTP request to url with retry and delay if needed.

    The sending data should be json. Otherwise, you have to specific headers to send request. 

    If not silent:
        RetryLimitExceededException will be raised after max_retry retries.
    else:
        return None
    '''

    retry = 0
    while retry < max_retry:
        try:
            if isinstance(data, dict):
                res = requests.request(method, url, json=data, timeout=timeout, headers=headers)
            elif data is not None:
                res = requests.request(method, url, data=data, timeout=timeout, headers=headers)
            else:
                res = requests.request(method, url, timeout=timeout, headers=headers)
            return res
        except requests.exceptions.RequestException:
            retry += 1
            sleep(delay)

    if not silent:
        raise RetryLimitExceededException(f"Unable to send request after {max_retry} retries.")

    return None


