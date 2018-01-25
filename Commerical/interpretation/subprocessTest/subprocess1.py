# ！/usr/bin/env python3


import re, os, sys
import subprocess
import time
'''
class subprocess.Popen(args, bufsize=-1, executable=None, stdin=None, stdout=None,
stderr=None, preexec_fn=None, close_fds=True, shell=False, cwd=None, env=None,
universal_newlines=False, startupinfo=None, creationflags=0, restore_signals=True,
start_new_session=False, pass_fds=(), *, encoding=None, errors=None)
'''
# args:命令行参数，可以是sequence也可以是string，例如['ls','-l']或者'ls'或者'ls -l'都可以
args1 = ['ls', '-l']
args2 = 'ls'
args3 = 'ls -l'
args4 = '-l'

# subprocess.Popen(args1)
# subprocess.Popen(args2)
# subprocess.Popen(args3)
# 3会出错，因为string不是一个可以直接执行（这个不是很理解，但是一定会出错就对了）
# 这就需要添加一个executable或者shell参数
# subprocess.Popen(args3,executable='pwd')
# print('args:'+subprocess.Popen(args3,executable='pwd').args)

# subprocess.Popen(args4,executable='ls',shell=False)
# subprocess.Popen(args4,executable='ls')


# bufsize:输出时，缓存大小，-1表示和系统设置相同，1表示一行一输出，0表示有多少输出多少，其他正数
# 表示缓存大小
# subprocess.Popen(args1,bufsize=-1)


# stdin 标准输入，和命令行参数输入有差异，可以用subprocess.PIPE进行初始化
# cwd 就是在执行命令之前，先把路径转换到这个路径下

args5 = ['perl', 'subprocess.pl']
args6 = ['perl','subprocess2.pl']
args7='cat'

# subprocess.pl
'''
print "subprocess2.pl\n";
'''

# subprocess2.pl的内容
'''
print "title:做个小实验\n";
'''

P1 = subprocess.Popen(args5, stdout=subprocess.PIPE, shell=False,
                     cwd='/annoroad/data1/bioinfo/PROJECT/RD/Medical/Leukemia/V2_panel/'
                         'test12_RERUN_20160120/chenyuelong/tmp')
# out,err = P1.communicate()
# print('gggggg'+out.decode())
# print(out)
# P1.wait()

P2 = subprocess.Popen(args6,stdin=subprocess.PIPE,stdout=subprocess.PIPE,shell=False,
                      cwd='/annoroad/data1/bioinfo/PROJECT/RD/Medical/Leukemia/V2_panel/'
                          'test12_RERUN_20160120/chenyuelong/tmp')

out,err = P2.communicate(b'uuuuuuuuuu')
print(out.decode())
# print(P2.args)
# P3 = subprocess.Popen(args7,stdin=P2.stdout,stdout=subprocess.PIPE)
# print(P3.poll())
# print(P3.pid)
# time.sleep(2)
# print(P3.poll())
# P3.wait()
# testo,teste =P3.communicate()
# print(testo.decode())
# print(P3.pid)
# P = subprocess.Popen(args1, stdout=subprocess.PIPE)
# returncode = P.wait()
# print(returncode)
# print(P.stdout)
#
#
#
# P1 = subprocess.Popen(args1, stdout=subprocess.PIPE)
# # P1.wait()
# testout,testerr=P1.communicate()
#
#
# print('test:{}:{}'.format(testout.decode(),type(testerr)))

#
# child = subprocess.Popen(["cat"], stdin=subprocess.PIPE)
# child.communicate(b"vamei")

