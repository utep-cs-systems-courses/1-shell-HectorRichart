import sys 
import os
import re 

def main():
    #Printing prompt and reading command as long as user doesnt type exit
    while(True):
        commandToExecute = input("\n$")
        if commandToExecute == "exit":
            break
        #Making sure the first 3 character of the command to read entered by the user is cd and a space
        elif commandToExecute[:3] == "cd ":
            #Executing the command input starting from position 3
            cd_command(commandToExecute[3:])
            #print error message if command does not exist
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

if '__main__' == __name__:
    main()