

if __name__ == '__main__':
    # use shlex.split to split command string into array
    import shlex
    import subprocess

    cmd = 'ls -la'
    subprocess.call(shlex.split(cmd))