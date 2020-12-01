import os
import ntpath
from pathlib import Path
from ftplib import FTP, error_perm


class FTPWrapper():
    def __init__(self, host, user, password, base_dir):
        self._ftp = FTP(host, user, password)

        self._base_dir = base_dir

    def download(self, ftp_src, des, filename=None):
        '''
        Download file from FTP server and save it to destination (directory)

        Args:
            - ftp_src: The relative src path in FTP server
            - des: The destionation directory to save
            - filename: 
        '''

        if not filename:
            filename = ntpath.basename(ftp_src)
        
        src_file_path = self._base_dir + ftp_src

        des_file_path = os.path.join(des, filename)

        # if des is not exists, create des
        Path(des).mkdir(parents=True, exist_ok=True)

        # start downloading file
        with open(des_file_path, 'wb') as f:
            self._ftp.retrbinary(f'RETR {src_file_path}', f.write)
    

    def upload(src, ftp_des, filename=None):
        '''
        Upload file from src to FTP des (directory)

        Args: 
            - ftp_des: The relative path of directory in FTP server
            - src: The absolute path of file to upload
        '''

        if not filename:
            filename = ntpath.basename(src)
        
        des_file_path = os.path.join(ftp_des, filename)

        # start uploading file
        self._ftp.storbinary(f'STOR {des_file_path}', open(src, 'rb'))
