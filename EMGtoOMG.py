# BuildSeq Function - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - -
def buildSeq(seq,sig1,sig2,sig3):

    # First function called by

    # If the last digit in the sequence is a 0,
    # program is prepared to receive next signal

    if seq[-1] == 0:
        
        if sig1 == 1:
            seq[-1]=1
            seq.append(-1)
            return
        
        elif sig2 == 1:
            seq[-1]=2
            seq.append(-1)
            return
        
        elif sig3 == 1:
            seq[-1]=3
            seq.append(-1)
            return

    # If the last digit in the sequence is a -1,
    # program is waiting for signals to be released

    elif seq[-1] == -1:
        if sig1 == 0 and sig2 == 0 and sig3 == 0:
            seq[-1] = 0
            return

        else:
            return

    else:
        return

# - - - - - - - - - - - - - - - - - - - - - - - - -



# Directory Function  - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - -
def directory(seq,c,state,setID,charSearch,output):

    # seq is the growing array storing the unique
    # 'sequence' of signal inputs

    # c is the 'cursor' and tracks where in the seq
    # the program is currently looking

    # state refers to which funciton the program is
    # currently processing
    # 1-"Unknown" is waiting for a proper input
    # 2-"Find" is logging the set ID
    # 3-"Nav" means in a set and parsing through it

    # setID is the up to 3-element array storing the
    # set ID

    # charSearch is the array stores the cycling
    # through an array until a character is chosen

    # output is the translated text

    # If the last digit is a 0, the function is
    # waiting for next signal.
    # If the last digit is a -1, the function is
    # waiting for all signals to be released.
    if seq[c[0]] <= 0:
        return 
    
    # If a state has been assigned, redirect to
    # that function.
    elif state[0] == 1:
        unkSet(seq,c,state,setID)
        return
        
    elif state[0] == 2:
        findSet(seq,c,state,setID,output)
        return
        
    elif state[0] == 3:
        navSet(seq,c,state,setID,charSearch,output)
        return

    elif state[0] == 4:
        edit(seq,c,state,setID,charSearch,output)
        return

    else:
        return
# - - - - - - - - - - - - - - - - - - - - - - - - -



# unkSet Function  - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - -
def unkSet(seq,c,state,setID):

    # This code is called when the state is
    # "Unknown" and only changes the state to
    # "Find" when a 1 is encountered.
    if seq[c[0]] == 1:
        state[0] = 2
        setID[0]=1
        c[0] += 1
        return

    # If the cursor is on a 2 or 3, look at next
    elif seq[c[0]] == 2 or seq[c[0]] == 3:
        c[0] += 1
        return

    else:
        return
    
# - - - - - - - - - - - - - - - - - - - - - - - - -



# findSet Function  - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - -
def findSet(seq,c,state,setID,output):

    # This code is called when the state is "Find"
    # and changes to "Unknown" if setID is invalid
    # (1-1-1) or changes to "Nav" if setID is valid

    if len(setID) == 1:
        a = seq[c[0]]
        setID.append(a)
        c[0] += 1
        return
        
    elif len(setID) == 2:
        a = seq[c[0]]
        setID.append(a)

        # If the sequence is 1-1-1 then
        # reset and wait for new signal
        # Set state to Unknown and reset setID
        if setID[0] == 1 and setID[1] == 1 and setID[2] == 1:
            if len(output) == 2:
                state[0] = 1
                setID[0] = 0
                while len(setID) > 1:
                    del setID[1]
                c[0] += 1

            else:
                state[0] = 4
                setNum(setID)
                output[-2] = output[-3]
                output[-3] = "{"
                c[0] += 1
        
        else:
            state[0] = 3
            setNum(setID)
            output.insert(-1," ")
            c[0] += 1
            return

    else:
        return
    
# - - - - - - - - - - - - - - - - - - - - - - - - -



# navSet Function  - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - -
def navSet(seq,c,state,setID,charSearch,output):

    # This code is called when the state is "Nav"
    # and modifies the output as signals arrive.
    # Saves input and sets state to "Find" when
    # a 1 is registered. Saves input and keeps
    # state saved as "Nav" when a 2 is registered.
    # 1 = ^
    # 2 = <
    # 3 = >

    # output starts as { }

    # 3 means cycle through set
    if seq[c[0]] == 3:
        # log the input of 3
        # retrieve the set that was chosen
        charSearch.append(3)
        setX = retrieveSet(setID)

        # charSearch[0] holds the index of setX that
        # is being looked at
        charSearch[0] += 1
        if charSearch[0] == len(setX):
            charSearch[0] = 0

        # Show the new character being looked at
        i = charSearch[0]
        output[-2] = setX[i]

        c[0] += 1
        return

    # 2 means select, stay in set
    elif seq[c[0]] == 2:
        output[-3] = output[-2]
        output[-2] = "{"
        output.insert(-1," ")
        charSearch[0] = 0
        while len(charSearch) > 1:
            del charSearch[1]

        c[0] += 1
        return

    # 1 means select, choose new set
    elif seq[c[0]] == 1:
        output[-3] = output[-2]
        output[-2] = "{"
        charSearch[0] = 0
        while len(charSearch) > 1:
            del charSearch[1]
        setID[0]= 1
        while len(setID) > 1:
            del setID[1]
        state[0] = 2
        
        c[0] += 1
        return
# - - - - - - - - - - - - - - - - - - - - - - - - -



# SetNum- - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - -
def setNum(setID):

    if setID[1] == 1:

        if setID[2] == 1:
            setID.append(1)

        elif setID[2] == 2:
            setID.append(2)
            
        elif setID[2] == 3:
            setID.append(3)

    elif setID[1] == 2:

        if setID[2] == 1:
            setID.append(4)

        elif setID[2] == 2:
            setID.append(5)
            
        elif setID[2] == 3:
            setID.append(6)

    elif setID[1] == 3:

        if setID[2] == 1:
            setID.append(7)

        elif setID[2] == 2:
            setID.append(8)
            
        elif setID[2] == 3:
            setID.append(9)
# - - - - - - - - - - - - - - - - - - - - - - - - -



# retrieveSet Function  - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - -
def retrieveSet(setID):

    if setID[-1] == 2:
        str1 = ' abcdeABCDE'
        return(list(str1))
    
    if setID[-1] == 3:
        str2 = ' fghijkFGHIJK'
        return(list(str2))

    if setID[-1] == 4:
        str3 = ' lmnopLMNOP'
        return(list(str3))

    if setID[-1] == 5:
        str4 = ' qrstuQRSTU'
        return(list(str4))

    if setID[-1] == 6:
        str5 = ' vwxyzVWXYZ'
        return(list(str5))

    if setID[-1] == 7:
        str6 = ' .,?!>\'\"@#&_-+='
        return(list(str6))

    if setID[-1] == 8:
        str7 = ' ()[]<>/\|%^*~'
        return(list(str7))

    if setID[-1] == 9:
        str8 = ' 0123456789'
        return(list(str8))
    
# - - - - - - - - - - - - - - - - - - - - - - - - -



# edit Function  - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - -
def edit(seq,c,state,setID,charSearch,output):

    # This code is called when the state is
    # "Edit" and only changes the state to
    # "Find" when a 1 is encountered.
 
    if len(output) == 2 or seq[c[0]] == 1:
        if seq[c[0]] == 1:
            state[0] = 2
            setID[0] = 1
        elif len(output) == 2:
            state[0] = 1
            setID[0] = 0
        charSearch[0] = 0
        while len(charSearch) > 1:
            del charSearch[1]
        setID[0] = 1
        while len(setID) > 1:
            del setID[1]
        i = output.index('{')
        del output[i]
        output.append('{')
        i = output.index('}')
        del output[i]
        output.append('}')
        c[0] += 1

    # [0] == 0 cursor left
    elif charSearch[0] == 0:
        if seq[c[0]] == 3:
            charSearch.append(3)
            charSearch[0] = 1
            c[0] += 1

        elif seq[c[0]] == 2:
            charSearch.append(2)

            if output[0] == "{":
                c[0] += 1
                return

            i = output.index('{')
            output[i] = output[i-1]
            output[i+2] = output[i+1]
            output[i-1] = "{"
            output[i+1] = "}"
            c[0] += 1

    # [0] == 1 cursor right
    elif charSearch[0] == 1:
        if seq[c[0]] == 3:
            charSearch.append(3)
            charSearch[0] = 2
            c[0] += 1

        elif seq[c[0]] == 2:
            charSearch.append(2)

            if output[-1] == "}":
                c[0] += 1
                return

            i = output.index('{')
            output[i] = output[i+1]
            output[i+2] = output[i+3]
            output[i+1] = "{"
            output[i+3] = "}"
            c[0] += 1

    # [0] == 2 backspace
    elif charSearch[0] == 2:
        if seq[c[0]] == 3:
            charSearch.append(3)
            charSearch[0] = 0
            c[0] += 1
            
        elif seq[c[0]] == 2:
            charSearch.append(2)
            
            if output[0] == "{" and output[1] == "}":
                c[0] += 1
                return
            
            i = output.index('{')
            del output[i+1]
            
            if output[0] == "{":
                c[0] += 1
                return
            
            output[i] = output[i-1]
            output[i-1] = "{"
            c[0] += 1
# - - - - - - - - - - - - - - - - - - - - - - - - -



# ShowOutput Function  - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - -
def showOutput(output):

    # This code is called to convert the output
    # array into a string, and return it.
    
    return("".join(output))
# - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - -
def functest():
    a=1
# - - - - - - - - - - - - - - - - - - - - - - - - -



# - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - -
str1 = ' abcdeABCDE'
str2 = ' fghijkFGHIJK'
str3 = ' lmnopLMNOP'
str4 = ' qrstuQRSTU'
str5 = ' vwxyzVWXYZ'
str6 = ' .,!>\'\"@#&_-+='
str7 = ' ()[]<>/\|%^*~'
str8 = ' 0123456789'

set1 = list(str1)
set2 = list(str2)
set3 = list(str3)
set4 = list(str4)
set5 = list(str5)
set6 = list(str6)
set7 = list(str7)
set8 = list(str8)

testseq=[3,2,1,1,1,1,3,3,3,2,3,2,1,2,3,1,3,3,3,2,3,1,3,2,2,3,1,3]

testvar = 0


