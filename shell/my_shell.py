import sys 
import os

def main():
    while True:
        rc = os.fork()
    
        if rc < 0:
            sys.exit(1)
        
        elif rc == 0:
            os.write(1, ("$").encode())
            commandToExecute = os.read(1,100) 
        
            if commandToExecute.decode().strip() == "exit":
                sys.exit(0)
            
            elif commandToExecute[:3].decode().strip() == "cd":
                cd_command(commandToExecute[3:].decode().strip())
                          
            else:
                print(commandToExecute.decode().strip() + ": Command not found")

def cd_command(path):
    try:
        #changes to absolute path of the path we are passing as parameter
        os.chdir(os.path.abspath(path))
        print("Currently working on: " + os.getcwd())
    except Exception:
        print("cd: no such file or directory: {}".format(path))

if '__main__' == __name__:
    main()