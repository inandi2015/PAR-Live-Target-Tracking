def header():
    print('******************************************************************************')
    print('                             PROJECT LAZARUS')
    print('                                Version: 1')
    print('                          UML-ADI CAPSTONE 2018')
    print('We are very grateful to Mr. Benjamin Sam for his contributions to this project')
    print('******************************************************************************')

def usrOptions():
    print("\tFor Long Point & Check \t\t- \tEnter 1")
    print("\tFor Quick Point & Check \t- \tEnter 2")
    print("\tFor Long Sweep Scan \t\t- \tEnter 3")
    print("\tFor Quick Sweep Scan \t\t- \tEnter 4")
    print("\tFor Quick Steering \t\t- \tEnter 5") 
    print("\tFor Continous Steering \t\t- \tEnter 6")
    print("\tFor Help on Commands \t\t- \tEnter 7") 
    print("\tFor Exit Protocol \t\t- \tEnter 8 Or Type exit")
    print("\tFor Command Options \t\t- \tPress O \n")

def getCommand():
        Command = raw_input("Enter Command: ")
        return Command

def getHelp():
    print("Enter 100 if Frank is needed.")
    cmdNum = raw_input("Enter Command Number: ")
    if cmdNum == '1':
       print("\t\t Long Point & Check")
       print("This Command requests for an angle from you. The program steers the beam to the specified angle. \nA measurement is taken by opening the Waveforms GUI. The time for this process is approximately 1 min 30 secs")
       print("The time constraint is long because of the logistics involved in opening Waveforms")
    elif cmdNum == '2':
       print("\t\t Quick Point & Check")
       print("This Command requests for an angle from you. The program steers the beam to the specified angle. \nA measurement is taken by opening the Waveforms GUI. The time for this process shorter than 1.")
       print("This command uses direct interface with the Analog Discovery")
    elif cmdNum == '3':
       print("\t\t Long Sweep Scan")
       print("The program steers the beam from the far right to the far left. \nA measurement is taken by opening the Waveforms GUI. The time for this process is approximately 5 mins")
       print("The time constraint is long because of the logistics involved in opening Waveforms")
    elif cmdNum == '4':
       print("\t\t Quick Sweep Scan")
       print("The program steers the beam from the far right to the far left. \nA measurement is taken by directly interfacing with Waveforms GUI. The time for this process is shorter")
       print("This command uses direct interface with the Analog Discovery")
    elif cmdNum == '5':
       print("\t\t Quick Steering")
       print("This Command requests for an angle from you. The program steers the beam to the specified angle. \nA measurement is taken by directly interfacing with Waveforms GUI.")
       print("This command uses direct interface with the Analog Discovery")
    elif cmdNum == '6':
       print("\t\t Continous Steering")
       print("The program steers the beam from the far right to the far left. \nThis is done continously until the user presses ENTER.\n Spectrum can be viewed on Analog Discovery Waveforms")
       print("This command uses direct interface with the Analog Discovery")
    elif cmdNum == '7':
       print("\t\t Continous Steering")
       print("This option briefly explains what each command does by taking command ID")
    elif cmdNum == '8' or cmdNum == 'EXIT' or cmdNum == 'Exit' or cmdNum == 'exit':
       print("\t\t Continous Steering")
       print("This option exits the program")
    elif cmdNum == 'O' or cmdNum == '0':
       print("\t\t Continous Steering")
       print("This option lists the available command options")
    
    else:
        print("\t\t\tAsk Frank")
        print("\t\t\tGithub: francman")
        print("\t\t\tEmail: frankmanu500@gmail.com")
        print("\t\t\tLinkedIn: Frank Manu") 

