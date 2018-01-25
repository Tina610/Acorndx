#! /usr/bin/env python3

import sys, os
import paramiko


class SFTP():
    def __init__(self, ftpfile, filelocal, hostname, port=22, user='', password=''):
        self.ftpf = ftpfile
        self.localf = filelocal
        self.hostname = hostname
        self.port = port
        self.timeout = 60
        self.user = user
        self.password = password

    def get_file(self):
        con = paramiko.Transport((self.hostname,self.port))
        con.connect(username=self.user,password=self.password)
        sftp=paramiko.SFTPClient.from_transport(con)
        sftp.get(self.ftpf,self.localf)
        print('download {} to {}'.format(self.ftpf,self.localf))
        con.close()

if __name__ =='__main__':
    testftp = SFTP('/home/mountFTP/临床项目样本信息(项目管理部)/7.血液病基因检测/'
                   '血液病基因检测简表2017.xlsx',
                   '/annoroad/data1/bioinfo/PROJECT/RD/Medical/Leukemia/'
                   'V2_panel/test12_RERUN_20160120/chenyuelong/tmp/leu.xlsx',
                   '192.168.13.237',
                   port=22,
                   user='ftpuser',
                   password='123')
    testftp.get_file()