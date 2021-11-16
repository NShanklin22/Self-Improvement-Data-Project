#This program will serve as the main navigation program, all others will be called from here
#import user_input

#Prints the main welcome message
print('Welcome to Onward\u2122 - a self improvement data tracking program\n')
print('Menu Options:')

#Create the option menu
print('1 - Enter new data to the database')
print('2 - Read old data from the database')
print('3 - Exit the program')

#Asks the user for their input
while True:
    MenuSelect = input('\nSelect a menu option: ')
    if MenuSelect == '1':
        exit()
    elif MenuSelect == '2':
        exit()
    elif MenuSelect == '3':
        exit()
    else:
        print('Invalid selection')
