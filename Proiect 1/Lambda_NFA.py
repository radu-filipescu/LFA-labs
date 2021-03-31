f = open( "input.txt", "rt" )

str = f.read().split("\n")
N, M = int(str[0][0]), int(str[0][2])

# transitions will be kept in a dictionary with
# tuples as keys and lists as values
trans = {}

for i in range( 1, M + 1 ):
    str[i] = str[i].split()
    if not ( int(str[i][0]), str[i][2] ) in trans: 
        trans[ (int(str[i][0]), str[i][2]) ] = []
    trans[ ( int(str[i][0]), str[i][2] ) ].append( int(str[i][1]) )

start = int( str[M + 1] )
final_states = set()
for x in str[M + 2].split():
    final_states.add( int(x) )

no_of_inputs = int( str[M + 3] )

def Check_word( word ):
    curr_states = [ start ]
    
    # we'll use this array to retrace the way
    pre = [ 0 for i in range( N )]
    pre[start] = -1

    # check if the starting state has any lambda transitions
    if ( start, "#" ) in trans:
        for st in trans[(start, "#")]:
            curr_states.append( st )
            pre[st] = start
 
    for symbol in word:
        tmp = []
        for st in curr_states:
            if (st, symbol) in trans:
                for x in trans[ (st, symbol )]:
                    tmp.append( x )
                    pre[x] = st
               
        curr_states = tmp
        for st in curr_states:
            if ( st, "#" ) in trans:
                curr_states += trans[( st, "#" )]
                for x in trans[( st, "#" )]:
                    pre[x] = st

    #print( pre )

    for st in curr_states:
        if st in final_states: 
            x = st
            route = []
            while pre[x] != -1:
                route.append( x )
                x = pre[x]
            route.append( start )
                
            return 1, route
    
    return -1, []

for i in range( no_of_inputs ):
#for i in range( 0, 1 ):
    while str[M + 4 + i][-1] == ' ':
        str[M + 4 + i] = str[M + 4 + i][:-1]
    
    lst = []
    ans, lst = Check_word( str[M + 4 + i] )

    if ans == -1: print( "NU" )
    else:
        print( "DA" )
        lst.reverse()
        print( "Traseu: ", lst )

    
