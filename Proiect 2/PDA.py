
#PDA
#
#Cum arata fisierul:
#
##           <- caracterul pt lambda
#S           <- starea initiala
#A B C       <- starile
#C           <- starile finale
#a           <- alfabetul
#ASZ         <- alfabetul stivei
#Z           <- caracterul de la baza stivei
#
#            <- tranzitiile:
#S A a Z/ASZ    <-   Stare de unde se deplaseaza, noua stare, litera citita din cuvant, cum modifica stiva
#A A a A/AA    <-   Stare de unde se deplaseaza, noua stare, litera citita din cuvant, cum modifica stiva
#
#A B # A/A    <-   Stare de unde se deplaseaza, noua stare, litera citita din cuvant, cum modifica stiva
#B B # AAA/A
#B C # SZ/Z
#
#
#
#<- si vom valida doar cand si stiva ramane goala
#<- cu stare finala
#<- cu ambele
#
#
#1. Cititi PDA si salvati-l intr-o structura utila
#    (spre exemplu folosim @dataclass cu typing "ca lumea")
#2.


# input reading and sanitizing ( removing blank lines and some spaces )

f = open( "PDA.txt", "rt" )

inputfile = f.read().split("\n")

for i in range( len(inputfile) ):
    while len(inputfile[i]) > 0 and inputfile[i][-1] == " ":
        inputfile[i] = inputfile[i][:-1]

inputfile2 = []
for i in range( len(inputfile) ):
    if len(inputfile[i]) > 0:
        inputfile2.append( inputfile[i] )

inputfile = inputfile2;

lambda_char = inputfile[0]
initial_state = inputfile[1]
states = []
for x in inputfile[2].split():
    states.append( x )
final_states = []
for x in inputfile[3].split():
    final_states.append( x )
alpha = []
for x in inputfile[4].split():
    alpha.append( x )
stack_alpha = []
for x in inputfile[5].split():
    stack_alpha.append( x )

stack_base = inputfile[6]

# transitions will be represented in memory as a 
# dictionary with a tuple as key ( start_state, input_letter ) 
# and a list of 3-tuples as value ( stack_top, end_state, stack_add )

transitions = {}

for i in range( 7, len(inputfile) ):
    x = inputfile[i].replace( '/', ' ')
    x = x.split()
    
    start_state = x[0]
    end_state = x[1]
    input_letter = x[2]
    stack_top = x[3]
    if len(x) == 5:
        stack_add = x[4]
    else:
        stack_add = ""

    #print( start_state, input_letter, stack_top, end_state, stack_add )

    transitions[ ( start_state, input_letter ) ] = []
    transitions[ ( start_state, input_letter ) ].append( ( stack_top, end_state, stack_add ) )


current_states = []
current_states.append( initial_state )

validation_type = int( input( "Introduceti tipul validarii:\n\n1.Stiva goala\n2.Stare finala\n3.Ambele\n" ) )

pushdown_stack = stack_base

INPUT_WORD = input( "Introduceti cuvantul: \n")

accepted = False

def Backtrack( pos, curr_state ):
    global accepted
    global pushdown_stack

    #print( pos, curr_state )

    if validation_type != 2 and len(pushdown_stack) == 0:
        accepted = True

    #print( pos, curr_state )
    #print( pushdown_stack )
    #print()

    if accepted == True: return
    
    if pos == len( INPUT_WORD ):
        if validation_type == 1 and len( pushdown_stack ) == 0:
            accepted = True
        if validation_type == 2 and curr_state in final_states:
            accepted = True
        if validation_type == 3 and len( pushdown_stack ) == 0 and curr_state in final_states:
            accepted = True
        return

    if (curr_state, INPUT_WORD[pos] ) in transitions:
        for x in transitions[ (curr_state, INPUT_WORD[pos] ) ]:
            if len( pushdown_stack ) >= len( x[0] ):
                ok = True
                for i in range( len(x[0]) ):
                    if x[0][i] != pushdown_stack[len(pushdown_stack) - len(x[0]) + i]:
                        ok = False
                        break

                if ok:
                   save = pushdown_stack
                
                   pushdown_stack = pushdown_stack[:-len(x[0])]
                   pushdown_stack += x[2]

                   Backtrack( pos + 1 , x[1] )

                   pushdown_stack = save
    else:
        Backtrack( pos + 1, curr_state )
    if (curr_state, "#") in transitions:
        for x in transitions[ (curr_state, "#") ]:
            if len( pushdown_stack ) >= len( x[0] ):
                ok = True
                for i in range( len(x[0]) ):
                    if x[0][i] != pushdown_stack[ len(pushdown_stack) ][len(pushdown_stack) - len(x[0]) + i]:
                        ok = False
                        break

                if ok:
                   save = pushdown_stack
                
                   pushdown_stack = pushdown_stack[:-len(x[0])]
                   pushdown_stack += x[2]

                   Backtrack( pos , x[1] )

                   pushdown_stack = save

Backtrack( 0, initial_state )

if accepted:
    print( "accepted" )
else:
    print( "rejected" )
