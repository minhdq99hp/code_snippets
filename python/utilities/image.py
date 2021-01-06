'''
Utility functions for working with images.
Contributors: 
    - minhdq99hp@gmail.com
'''
import io
import requests
import traceback

from PIL import Image
from os.path import splitext

class UnsupportedExtension(Exception):
    pass

def convert_image(input_path, output_path, o_ext=None):
    '''
    Use PIL.Image to convert image format.
    The output extension will be determined from output_path. 
    You can also specify it by using o_ext.

    Supported extensions: png, jpeg, webp
    Warning: 
    - Every image will be convert to RGB, 
      which mean the output image will not have alpha value.
    '''
    supported_exts = ('png', 'jpeg', 'webp', 'bmp')
    if not o_ext:
        _, ext = splitext(output_path)
        o_ext = ext[1:].lower().replace('jpg', 'jpeg')

    if o_ext not in supported_exts:
        raise UnsupportedExtension(f"Can't convert image to {o_ext}")

    im = Image.open(input_path).convert("RGB")
    im.save(output_path, o_ext)


def download_image_from_url(url):
    """
    Return a dictionary contains data of the image

    Args:
        url (str): direct link of the image

    Returns:
        dict: result data of the image

            {
                'status': 0 if success, others if error occurs.
                'extension': the format of the image. Ex: png, jpeg,...
                'file': binary data of the image
            }
    """
    result = {'status': 1}
    try:
        res = requests.get(url, timeout=15, verify=False)
    except requests.exceptions.RequestException:
        traceback.print_exc()
        return result
    try:
        data = res.content
        im = Image.open(io.BytesIO(data))
        im.verify()

        result['extension'] = im.format.lower()
        result['file'] = data
    except Exception as e:
        traceback.print_exc()
        return result

    result['status'] = 0
    return result