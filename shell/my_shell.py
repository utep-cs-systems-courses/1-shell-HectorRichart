#!/usr/bin/env python3 
from base64 import decode
from operator import contains
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
         
        elif commandToExecute.__contains__("|"):
            pipe(commandToExecute)
            
        elif commandToExecute[0] == "cd": 
            cd_command(commandToExecute)
            continue        
          
        #Fork a child, check if correctly forked    
        rc = os.fork()
            
        if rc < 0:
            sys.exit(1)
                
        #Executing in child process because rc == 0 by fork definition
        elif rc == 0:           
            #Checking If output redirection
            if commandToExecute.__contains__(">"):
                os.close(1) #close stdout
                #If file specified in command[2] does not exist create it, otherwise write on it
                os.open(commandToExecute[2], os.O_CREAT|os.O_WRONLY)
                os.set_inheritable(1, True) #inheriting with flag code 1
                commandToExecute = commandToExecute[:1]
                
            #Checking if input redirection
            elif commandToExecute.__contains__("<"):
                os.close(0) #close stdin
                #opening specified file to read only
                os.open(commandToExecute[2], os.O_RDONLY)
                os.set_inheritable(0, True)
                commandToExecute = commandToExecute[:1]
            
            execute(commandToExecute)
 
    #wait for child to finish
        else: 
            childPidCode = os.wait()  
  
#helper funtion that takes care of executing the program  
def execute(path):
    # Search each directory in PATH
    for dir in re.split(":", os.environ['PATH']):
        # Obtain the program
        program = "%s/%s" % (dir, path[0])
        try:
            # Attemp to execute program, command at positon 0 of user input
            os.execve(program, path, os.environ)
        except FileNotFoundError:
            # Fail quitely lol
            pass                          
    # Terminate with error
    sys.exit(1)         
  
            
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

def pipe_helper(pr, pw, program, fd_type):
    # Checks for what to duplicate
    dup_this = pw if fd_type == 1 else pr

    #closing pipe depending on file descriptor 
    os.close(fd_type)
    #duplicates the corresponding pipe depending on file descriptor
    os.dup(dup_this)
    os.set_inheritable(fd_type, True)

    for file_descriptor in (pr, pw):
        execute(program)
    #sys.exit(1)

def pipe(path):
    pipe_split_index = path.index("|")
    write = path[0:pipe_split_index] #taking left side of the pipe (output used to write to pipe)
    read = path[pipe_split_index + 1:] #taking right side of the pipe (command to execute )
    pipe_read, pipe_write = os.pipe()#Creating a pipe for read and write 

    rc = os.fork()

    # This is the child (write side of pipe)~
    if rc == 0:
        pipe_helper(pipe_read, pipe_write, write, 1)

    # This is the child (read side of pipe)~
    elif rc > 0:
        pipe_helper(pipe_read, pipe_write, read, 0)

    else:
        sys.exit(1)

if '__main__' == __name__:
    main()
    