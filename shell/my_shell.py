#!/usr/bin/env python3 
from base64 import decode
from operator import contains
import sys 
import os
import re 


#PUSH CODE TO REPO
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
        else:
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
                    os.set_inheritable(0, True) #can inherit by child process, child will have same file descript as parent
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
            # Attemp to execute program, command at positon 0 of user input, use path
            os.execve(program, path, os.environ) #execve replaces memory of the current process
        except FileNotFoundError:
            pass                          
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

def pipe(command):
    pr, pw = os.pipe() #two pipes are needed to establish two way communication
    rc_1 = os.fork()

    if rc_1 < 0:
        sys.exit(1)

    elif rc_1 == 0: # writing
        os.close(1) # close standard output, parent write, child read
        os.dup(pw)
        os.set_inheritable(1, True)

        for fd in (pr, pw):
            os.close(fd)

        user_input = command[0:command.index("|")]
        execute(user_input)
        sys.exit(1)

    else: # reading
        rc_2 = os.fork() #parent read, child write

        if rc_2 < 0: # fork failed
            sys.exit(1)

        elif rc_2 == 0:  # reading
            os.close(0) # close standard input
            os.dup(pr)
            os.set_inheritable(0, True)

            for fd in (pr, pw):
                os.close(fd)

            user_input = command[command.index("|") + 1:]
            execute(user_input)
            sys.exit(1)
        else:
            childPidCode = os.wait()
        for fd in (pr, pw):
            os.close(fd)
        childPidCode = os.wait()


if '__main__' == __name__:
    main()
    