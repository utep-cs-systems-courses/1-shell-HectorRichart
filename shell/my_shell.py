#!/usr/bin/env python3 
from base64 import decode
import sys 
import os
import re 

def main():
    while True:
        #splitting user input, making it an array, printing prompt
        path = f"{os.getcwd()} $ "
        os.write(1, path.encode())
        #read user input, can read up to 1000 bytes, need to decode cause we get bytes back
        commandToExecute = os.read(0,1000).decode().split()
        
        if commandToExecute[0] == "exit":
            sys.exit(1)
            
        elif commandToExecute[0] == "cd": 
            cd_command(commandToExecute)
            continue                      
            
        #Fork a child, check if correctly forked    
        rc = os.fork()
            
        if rc < 0:
            sys.exit(1)
                
        #Executing in child process because rc == 0 by fork definition
        elif rc == 0:
            args = commandToExecute
            #checking if the user input contains > which means redirect
            if len(args) == 3 and args[1] == ">":
                #redirect child stdout
                os.close(1)             
                #if specified file given by args[2] doers not exist create it or open to write only   
                os.open(args[2], os.O_CREAT | os.O_WRONLY)
                
                os.set_inheritable(1, True)
            for dir in re.split(":", os.environ['PATH']):  # try each directory in the path
                program = "%s/%s" % (dir, args[0])
                #using execve command to run the program on the os environment
                try:
                    os.execve(program, args, os.environ)  # try to exec program

                except FileNotFoundError:
                        pass           
            sys.exit(1)      
    #wait for child to finish
        else: 
            childPidCode = os.wait()  
            
def cd_command(path):
    #if the len is > 1, will change to directory in index 1 of the command array 
    if len(path) > 1:
        try:
            os.chdir(path[1])
            #if specified directory does not exist
        except Exception:
            print("cd: no such file or directory: {}".format(path[1]))
     #Takes us to the very main directory (cd, will go here if input is cd and just 1 thing in list)
    else:
       os.chdir(os.path.expanduser("~"))   
       

if '__main__' == __name__:
    main()