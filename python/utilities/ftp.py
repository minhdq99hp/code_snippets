import os
import ntpath
import traceback
from pathlib import Path
from ftplib import FTP, error_perm, all_errors


class FTPWrapper():
    MAX_RETRY = 3

    def __init__(self, host, user, password, base_dir, timeout=None):
        self._base_dir = base_dir

        self._host = host
        self._user = user
        self._password = password
        self._timeout = timeout

        self.connect()

    def connect(self):
        self._ftp = FTP(self._host, self._user, self._password, self._timeout)
        # self._ftp.set_pasv(True)
        print("Connected to FTP server.")
    
    def close(self):
        self._ftp.close()

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
        retry = 0
        while retry < self.MAX_RETRY:
            try:
                with open(des_file_path, 'wb') as f:
                    self._ftp.retrbinary(f'RETR {src_file_path}', f.write)
                break
            except all_errors:
                retry += 1
                traceback.print_exc()
                self.close()
                self.connect()

    def upload(self, src, ftp_des, filename=None):
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
        retry = 0
        while retry < self.MAX_RETRY:
            try:
                self._ftp.storbinary(f'STOR {des_file_path}', open(src, 'rb'))
                break
            except all_errors:
                retry += 1
                traceback.print_exc()
                self.close()
                self.connect()