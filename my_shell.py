from multiprocessing import parent_process
import sys 
import os

def main():
    #Printing prompt and reading command as long as user doesnt type exit
    while(True):
        # commandToExecute = input("$")
        commandToExecute = input("$")
        if commandToExecute == "exit":
            sys.exit(0)
        #Making sure the first 3 character of the command to read entered by the user is cd and a space
        elif commandToExecute[:3] == "cd ":
            #Executing the command input starting from position 3
            cd_command(commandToExecute[3:])
            #print error message if command does not exist
        elif commandToExecute.__contains__(">") or commandToExecute.__contains__("<"):
            redirect()
        elif commandToExecute == "clear" or commandToExecute == "clear ":
            clear()

        else:
            print(commandToExecute + ": Command not found")


def cd_command(path):
    try:
        #using os library and built in functions to change directories passing the path as parameter 
        #changes to absolute path of the path we are passing as parameter
        os.chdir(os.path.abspath(path))
        #printing current directory for user using getcwd
        print("Currently working on: " + os.getcwd())
        #if directory doesnt exist print it along with the directory that was
        #tried to access, format(path) sends this tried directory to print message
    except Exception:
        print("cd: no such file or directory: {}".format(path))


def redirect(command):
    print(os.getpid())
    


#clears the temrinal
def clear():
    os.system("clear")

if '__main__' == __name__:
    main()