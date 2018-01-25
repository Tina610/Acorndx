#! /usr/bin/
from Leu_anno import extractFromFTP
import os, sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--ftpfile', '-f', help='The path of file in the FTP', action='store',
                    dest='ftpf', default='')
parser.add_argument('--localfile', '-lf', help='The file in local to get file in FTP', action='store',
                    dest='localf', default='')
parser.add_argument('--hostname', '-host', help='FTP Hostname', action='store',
                    dest='hostname', default='')
parser.add_argument('--port', '-p', help='Port', action='store',
                    dest='port', default=22)
parser.add_argument('--username', '-u', help='username', action='store',
                    dest='username', default='')
parser.add_argument('--password', '-pwd', help='Password', action='store',
                    dest='pwd', default='')
args = parser.parse_args()

if args.ftpf == '' or args.localf == '' or \
                args.hostname == '' or args.username == '' or args.pwd == '':
    print('Please input parameters:')
    print('--help or -h for help!')
    print(parser.parse_args(['-h']))
    sys.exit(0)


def main():
    ftpd = extractFromFTP.SFTP(args.ftpf, args.localf, args.hostname,
                               int(args.port), args.username, args.pwd)
    ftpd.get_file()

if __name__ == '__main__':
    main()
