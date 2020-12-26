'''
Utility function for working with files
Contributors: 
    - minhdq99hp@gmail.com
'''
import yaml
import json

def load_yaml(filepath, mode='r', encoding='utf-8'):
    with open(filepath, mode, encoding=encoding) as f:
        data = yaml.full_load(f)
        return data

def save_yaml(data, filepath, mode='w', encoding='utf-8'):
    with open(filepath, mode, encoding=encoding) as f:
        yaml.dump(data, f)

def load_json(filepath, mode='r', encoding='utf-8'):
    with open(filepath, mode, encoding=encoding) as f:
        data = json.load(f)
        return data

def save_json(data, filepath, mode='w', encoding='utf-8'):
    with open(filepath, mode, encoding=encoding) as f:
        json.dump(data, f, indent=4)

def remove_directory_contents(path):
    for path in Path(path).glob("**/*"):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            rmtree(path)

if __name__ == '__main__':
    # remove file safely (atomic operation)
    # require python 3.8+
    from pathlib import Path
    my_file = Path('./text.txt')
    my_file.unlink(missing_ok=True)


    # create folder recursively
    Path(des).mkdir(parents=True, exist_ok=True)

    # clear folder not so safely
    import os
    import shutil
    if os.path.isdir(folder_location):
        shutil.rmtree(folder_location)

    time.sleep(.5)  # to prevent error
    os.makedirs(folder_location, 0o777)

