'''
Utility functions for working with images.
Contributors: 
    - minhdq99hp@gmail.com
'''
from PIL import Image
from os.path import splitext

class UnsupportedExtension(Extension):
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
