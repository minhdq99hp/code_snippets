'''
Utility functions for working with requests
Contributors: 
    - minhdq99hp@gmail.com
'''
import os
import traceback
from uuid import uuid4
from PIL import Image
from pathlib import Path
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



class UnexpectedFileFormat(Exception):
    pass

class NotSupportedType(Exception):
    pass

def download_file_from_url(url, expected_type, timeout=60, output_dir='', valid_formats=None, valid_modes=None, auto_convert=True):
    '''
    Download file and write it to output_path.

    Args:
        url (str): direct link of the file
        expected_type: the expected type of the file, must be specify to guess the extension.

    Return:
        dict: 
        {
            'status': 0 if success
            'extension': e.g. jpg, png, wav, avi. Return None if the format can be guessed.
            'path': the downloaded filepath
        }

    Features:
    - Retrict memory usage

    '''
    result = {'status': 1}
    filename = f'{uuid4()}'
    filepath = os.path.join(output_dir, filename)
    extension = None

    # try to download the file
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    #if chunk: 
                    f.write(chunk)
    except requests.exceptions.RequestException:
        traceback.print_exc()

        # remove file safely (atomic operation)
        my_file = Path(filepath)
        my_file.unlink(missing_ok=True)
        return result

    if expected_type == 'image':
        try:
            if valid_formats is None:
                valid_formats = ['png', 'jpg']
            if valid_modes is None:
                valid_modes = ['RGB']
            # verify whether if image is not corrupted
            im = Image.open(filepath)
            im.verify()

            if im.mode not in valid_modes:
                im = im.convert('RGB')
                im.save(filepath)

            # get the extension
            extension = im.format.lower()
            if extension == 'jpeg':
                extension = 'jpg'
            
            
        except Exception:
            traceback.print_exc()
            return result
    elif expected_type == 'video':
        try:
            # TODO: verify and get the extension
            pass

            if valid_formats is None:
                valid_formats = ['mp4', 'avi']
    
        except Exception:
            
            traceback.print_exc()
            return result
    elif expected_type == 'sound':
        try:
            # TODO: verify and get the extension
            
            if valid_formats is None:
                valid_formats = ['mp3', 'wav']
            
        except Exception:
            traceback.print_exc()
            return result
    elif expected_type == 'text':
        try:
            # TODO: verify and get the extension
            pass

            if valid_formats is None:
                valid_formats = ['', None]
    
        except Exception:
            traceback.print_exc()
    elif expected_type is None:
        # check nothing, user have to decide the extension of the downloaded file.
        pass
    else:
        raise NotSupportedType(f'Type {expected_type} is not supported.')

    if extension not in valid_formats:
        if auto_convert:
            if expected_type == 'image':
                # convert 'webp' to 'png'
                if extension == 'webp':
                    im = Image.open(filepath)
                    im.save(filepath, 'png')


        raise UnexpectedFileFormat(f'Format {extension} is not expected.')
    
    result['path'] = filepath
    result['filename'] = filename
    result['extension'] = extension
    result['status'] = 0
    return result
