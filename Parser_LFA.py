import sys

args = sys.argv

if len( args ) != 2:
   print( "Invalid number of arguments" )

config_file = args[0]

#####
#config_file = "input.txt"
#####

f = open( config_file, "rt" )

inpt = f.read().split("\n")

words = []
states = []
transitions = {}

def State_in_list( x ):
    for st in states:
        if st[0] == x: return True
    return False

w = 0
s = 0
t = 0

valid = 1
start_count = 0

for line in inpt:
    if len(line) == 0: continue 
    if line[0] == '#': continue 

    line = line.replace(' ', '' )
  
    if line == "End": w = s = t = 0

    if w == 1: words.append( line )
    if s == 1: 
        start_state = 0
        end_state = 0
        line = line.split(',')
        
        if len(line) > 1:
            if 'F' in line:
                end_state = 1
            if 'S'in line:
                start_state = 1
                start_count += 1

        tmp = []
        tmp.append( line[0] )
        if end_state: tmp.append( 'E' )
        if start_state: tmp.append( 'S' )

        states.append( tmp )
    if t == 1: 
        line = line.split(',')

        if State_in_list(line[0]) and State_in_list(line[2]) and line[1] in words:
            transitions[ ( line[0], line[1] )] = line[2]
        else: valid = 0

    if line == "Sigma:": w = 1
    if line == "States:": s = 1
    if line == "Transitions:": t = 1

if start_count != 1: valid = 0

if not valid: print( "Input not valid" )
#else:
#    print( words )
#    print( states )
#    print( transitions )

current_state = ""
for x in states:
    if 'S' in x:
        current_state = x[0]
        break

test_word = args[1]
#test_word = input( "INPUT WORD: ")

for symb in test_word:
    if ( current_state, symb ) in transitions:
        current_state = transitions[ (current_state, symb ) ]

for st in states:
    if st[0] == current_state:
        if 'E' in st:
            print( "accepted" )
        else:
            print( "rejected")
        break






