import os
import subprocess

from subprocess import PIPE, run

def out(command):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result.stdout

def test(temp:str=None, temp2:str=None):
    print(f'---{temp}')

    if temp:
        print(f'---1 {temp}')
    else:
        print(f'---2 {temp}')



if __name__ == "__main__":
    # temp = os.system("ip link set dev can0 up")
    # print(f' --- {temp}')


    #output = out("pwd")
    #print(f' --- {output}')

    temp = '  0x00	STAT_CHK_NONE	        Function Test Init 전 (테스트 전)'

    print(temp.split()[1])
    print(temp.split()[2])

    temp = ''
    test(temp)