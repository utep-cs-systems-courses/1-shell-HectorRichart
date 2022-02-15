#!/usr/bin/env python3 

from base64 import decode
import sys 
import os

def main():
    while True:
        if "PS1" in os.environ:
            os.write(1, str.encode(os.environ["PS1"]))
        else:
            os.environ["PS1"] = "$"
            os.write(1, str.encode(os.environ["PS1"]))
        # pid = os.getpid()
        #splitting user input, making it an array
        path = f"{os.getcwd()} $ "
        os.write(1, path.encode())
        commandToExecute = os.read(0,1000).split()
        
        if commandToExecute[0].decode() == "exit":
            sys.exit(0)
            
        elif commandToExecute[0].decode() == "cd": 
            cd_command(commandToExecute) 
                       
        else:
            rc = os.fork()
            
            
                          
# def execute_command(command):
#     pid = os.getpid()
#     rc = os.fork()
#     if rc < 0:
#         os.write(2, ("fork failed, returning %d\n" % rc).encode())
#         sys.exit(1)    
            
#     elif rc == 0:
#         os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % 
#             (os.getpid(), pid)).encode())
#         #check if input contains < or >
#         #code redirection of input or output
       
def cd_command(path):
    #if the len is > 1, will change to directory in index 1 of the command array 
    if len(path) > 1:
        try:
            os.chdir(path[1])
        except Exception:
            print("cd: no such file or directory: {}".format(path[1].decode()))
     #Takes us to the very main directory (cd, will go here if input is cd and just 1 thing in list)
    else:
       os.chdir(os.path.expanduser("~"))   

if '__main__' == __name__:
    main()