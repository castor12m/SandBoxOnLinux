import time
import zmq
import typer

import argparse

# def main(t: bool = False, client: bool = False, clientSend: bool = False, pub: bool = False, sub: bool = False):
#     if t:
#         typer.echo(f"Use Server")

#     if client:
#         typer.echo(f"Use Client")

#     if clientSend:
#         typer.echo(f"Use ClientSend")

#     if pub:
#         typer.echo(f"Use Publisher")

#     if sub:
#         typer.echo(f"Use Subscriber")

def ___exe_test_ArgParse(args):
    try:
        parser = argparse.ArgumentParser(description='GSE Test Application CLI Mode')
        parser.add_argument('-t', '--test', help='input target test command')
        parser.add_argument('-a', '--argument', help='input target test argument')
        parser.add_argument('--loop', help='loop test option with number')
        parser.add_argument('-w', '--wholetestenable', help='test whole script', action='store_true')
        parser.add_argument('-u', '--userdata', help='input userdata')
        parser.add_argument('-m', '--matchdata', help='input matchdata')
        
        parser.error = __print_help
       
        rtn = __argumentSplit(args)
        
        result = parser.parse_args(rtn)

        return result
    
    except Exception as ex: 
        print(f'exp : {ex}')

def __print_help(errmsg):
   print(errmsg.split(' ')[0])

def __argumentSplit(args):
    result = []

    argsSplit = args.split()
    strBuffer = ''
    quoteFlag = False

    for i in range(len(argsSplit)):

        part = argsSplit[i]

        #if part.find('\'') or part.find('\"'):
        if '\'' in part or '\"' in part:            

            if strBuffer:
                quoteFlag = False
                strBuffer += f' {part}'
                strBuffer = strBuffer.replace('\'','')
                strBuffer = strBuffer.replace('\"','')
                result.append(strBuffer)   
                strBuffer = '' 
            else:
                quoteFlag = True
                strBuffer = part

        elif quoteFlag:
            strBuffer += f' {part}'
        else:
            result.append(part)
            
    return result

if __name__ == "__main__":
    #typer.run(main)
    rtn = ___exe_test_ArgParse('-t 0 -u \'01 02\'')

    if rtn.test:
        #print(f'----- test {rtn.test} ')
        print()

    #print(f'----- test {rtn.test} ')
    print()

    num = 3
    tx = "333 %02i" % (num)
    tx += " " + str(num)
    
    print(tx)
        
    