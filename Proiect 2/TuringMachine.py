# input reading and sanitizing

f = open( "Turing.txt", "rt" )

inputfile = f.read().split("\n")

for i in range( len(inputfile) ):
    while len(inputfile[i]) > 0 and inputfile[i][-1] == " ":
        inputfile[i] = inputfile[i][:-1]

inputfile2 = []
for i in range( len(inputfile) ):
    if len(inputfile[i]) > 0:
        inputfile2.append( inputfile[i] )

inputfile = inputfile2;

initial_state = inputfile[0]
final_state = inputfile[1]

transitions = {}

# transitions will be represented in memory as a 
# dictionary with a tuple as key ( start_state, input_letter ) 
# and a list of 3-tuples as value ( end_state, write_on_tape, move_on_tape )

for i in range( 2, len(inputfile) ):
    x = inputfile[i].split(",")

    start_state = x[0]
    tape_read = x[1]
    end_state = x[2]
    write_on_tape = x[3]
    move_on_tape = x[4]

    if ( start_state, tape_read ) not in transitions:
        transitions[( start_state, tape_read )] = []

    transitions[ ( start_state, tape_read ) ].append( ( end_state, write_on_tape, move_on_tape ) )

# to simulate an infinite tape we'll use two
# dinamically allocatted lists
# The first one handles the positive "indices" ( from 0 to +infinity )
# and the second one the negative ones

tape_head = 0
tape = []

# direction == 1  ( right )
# direction == 2  ( left )
def Move( direction ):
    global tape_head
    global tape

    if direction == 1:
        tape_head += 1
    else:
        tape_head -= 1

def Write( character ):
    global tape
    global tape_head
    
    if tape_head >= len(tape):
        tape.append('_')

    tape[tape_head] = character

def Read():
    global tape
    global tape_head

    if tape_head >= len(tape):
        tape.append( '_' )

    return tape[tape_head]

accepted = False

def Backtrack( current_state ):
    global accepted
    global final_state
    global tape_head
    global tape

    #print( current_state, tape_head )

    if current_state == final_state:
        accepted = True

    if accepted: return
    
    if ( current_state, Read() ) in transitions:
        for x in transitions[ (current_state, Read()) ]:
            save_current = tape_head
            save_tape = tape

            next_state = x[0]
            Write( x[1] )

            if x[2]  == '<':
                Move( 2 )

            if x[2] == '>':
                Move( 1 )

            Backtrack( next_state )

            tape_head = save_current
            tape = save_tape
    #else:
        #Backtrack( current_state )

while True:
    console_in = input( "Introdu cuvantul de input: ")

    if console_in == "quit":
        break

    accepted = False
    tape = [x for x in console_in]
    tape_head = 0
    current_state = initial_state

    Backtrack( initial_state )

    if accepted: print( "Accepted" )
    else: print( "Rejected" )
