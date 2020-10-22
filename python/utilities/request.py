'''
Utility functions for working with requests

Author: minhdq99hp@gmail.com
'''
import requests
from time import sleep

class RetryLimitExceededException(Exception):
    pass

def send_json_request(url, data={}, timeout=60, max_retry=3, delay=0, silent=True):
    '''Send a request with json data to url'''
    
    retry = 0
    while retry < max_retry:
        try:
            res = requests.post(url, json=data, timeout=timeout)
            return res
        except requests.exceptions.RequestException:
            retry += 1
            sleep(delay)

    if not silent:
        raise RetryLimitExceededException(f"Unable to send json request after {max_retry} retries.")

    return None

