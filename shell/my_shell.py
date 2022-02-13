import sys 
import os
import re

def main():
  
    while True:
        #splitting user input, making it an array
        path = f"{os.getcwd()} $ "
        os.write(1, path.encode())
        commandToExecute = os.read(0,1000).split()
        
        if commandToExecute[0].decode() == "exit":
            sys.exit(0)
            
        elif commandToExecute[0].decode() == "cd": 
            cd_command(commandToExecute)        
    # while True:
        # rc = os.fork()
        
        # if rc < 0:
        #     sys.exit(1)
        
        # elif rc == 0:
        #     # os.write(1, ("$").encode())
        #     # commandToExecute = os.read(1,100).strip().split()[0]

        #     # else:
        #     #     print(commandToExecute[0].decode()+ ": Command not found")

        #     args = commandToExecute

        #     for dir in re.split(":", os.environ['PATH']):  # try each directory in the path
        #         program = "%s/%s" % (dir, args[0])
        #         try:
        #             os.execve(program, args, os.environ)  # try to exec program

        #         except FileNotFoundError:  # ...expected
        #             pass  # ...fail quietly
        #     #os.write(2, ("Child:    Could not exec %s\n" % args[0]).encode())
        #     sys.exit(1)
        # else:  # parent (forked ok)
        #     childPidCode = os.wait()

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