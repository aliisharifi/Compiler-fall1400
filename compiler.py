def addToken(token, lexeme_temp, line):
    if line not in tokens:
        tokens.update({line: []})
    tokens[line].append((token, lexeme_temp))


def addError(lexeme_temp, error, line):
    if line not in errors:
        errors.update({line: []})
    errors[line].append((lexeme_temp, error))


def addSymbolTable(lexeme_temp):
    symbolTable.update({len(symbolTable) + 1: lexeme_temp})


def initSymbolTable():
    for x in keywords:
        symbolTable.update({len(symbolTable) + 1: x})


# Todo
################
"""
letter = [chr(i) for i in range(ord('a'), ord('z') + 1)]
letter = letter + [chr(i) for i in range(ord('A'), ord('Z') + 1)]

digit = [i for i in '0123456789']

whitespace = [i for i in '\n\t\f\r \v']

after_id_acc = [i for i in '()[]{}']
after_id_acc += whitespace
"""
table = {}
################
# defining sets
digit = [i for i in '0123456789']
lowercase_letters = {chr(i) for i in range(ord('a'), ord('z') + 1)}
uppercase_letters = {i.upper() for i in lowercase_letters}
letter = lowercase_letters + uppercase_letters
after_id_acc = {' ', '=', '<'} # TODO complete
after_num_acc = {} # TODO complete
symbol_except_eq = {i for i in ';:,[]()+-*<'}
whitespace = {i for i in ' \n\r\t\v\f'}
alphabet = {chr(i) for i in range(32, 127)} + whitespace + ''  # all printable ASCIIs

#TODO defining others!
start_other = {}
ID_KEY_other = {}
NUM_other = {}


#initializing table
table.update('start') = {}
for i in letter:
    table['start'].update(i) = 'ID_KEY'
for i in digit:
    table['start'].update(i) = 'NUM'
for i in symbol_except_eq:
    table['start'].update(i) = 'symbol_1'
table['start'].update('=') = 'symbol2'
table['start'].update('/') = 'COM_1'
for i in whitespace:
    table['start'].update(i) = 'whitespace'
table['start'].update('*') ='v' #TODO Check V?

for i in letter + digit:
    table['ID_KEY'].update(i) = 'ID_KEY'
for i in after_id_acc:
    table['ID_KEY'].update(i) = 'ID_KEY_ACC_*'
for i in ID_KEY_other:
    table['ID_KEY'].update(i) = 'invalid_input'

for i in digit:
    table['NUM'].update(i) = 'NUM'
for i in after_num_acc:
    table['NUM'].update(i) = 'NUM_ACC_*'
for i in NUM_other:
    table['NUM'].update(i) = 'invalid_number'

table['symbol_2'].update('=') = 'symbol_3'
for i in alphabet - {'='}:
    table['symbol_2'].update(i) = 'symbol_4_*'

for i in alphabet - {'/', '*'}:
    table['COM_1'].update(i) = 'invalid_input_*'
table['COM_1'].update('*') = 'COM_2'
table['COM_1'].update('/') = 'COM_4'

for i in alphabet - {'', '*'}:
    table['COM_2'].update(i) = 'COM_2'
table['COM_2'].update('') = 'unclosed_comment'
table['COM_2'].update('*') = 'COM_3'

for i in alphabet - {'', '\n'}:
    table['COM_4'].update('i') = 'COM_4'
table['COM_4'].update('') = 'COM_2_ACC'
table['COM_4'].update('\n') = 'COM_2_ACC'

for i in alphabet - {'', '/'}:
    table['COM_3'].update(i) = 'COM_2'
table['COM_3'].update('') = 'unclosed_comment'
table['COM_3'].update('/') = 'COM_2_ACC'

for i in alphabet - {'/'}:
    table['V'].update(i) = 'invalid_input_*'
table['/'].update('/') = 'unmatched_comment'
#################

lineCount = 1
state = ""
tokens = {}
errors = {}
symbolTable = {}
keywords = ["if", "else", "void", "int", "repeat", "break", "until", "return"]
openComment = False
startComment = -1
getNextToken = True

initSymbolTable()

f = open('input.txt', 'r')
inputLine = f.read()

# tempError = []
# tempToken = []
i = 0

while getNextToken and i <= len(inputLine):
    lexeme = ""
    state = "start"
    while True:
        if inputLine[i] in table[state]:
            state = (table[state])[inputLine[i]]
        else:
            state = (table[state])["other"]
        lexeme += inputLine[i]
        flag = 0
        if state == "ID_KEY_ACC_*":
            lexeme = lexeme[0: len(lexeme) - 1]
            if lexeme in keywords:
                addToken("KEYWORD", lexeme, lineCount)
            else:
                addToken("ID", lexeme, lineCount)
                addSymbolTable(lexeme)
            i -= 1

        elif state == "invalid_input":
            addError(lexeme, "Invalid input", lineCount)

        elif state == "invalid_input_*":
            addError(lexeme[0: len(lexeme) - 1], "Invalid input", lineCount)
            i -= 1

        elif state == "invalid_number":
            addError(lexeme, "Invalid number", lineCount)

        elif state == "NUM_ACC_*":
            addToken("NUM", lexeme[0: len(lexeme) - 1], lineCount)
            i -= 1

        elif state == "unmatched_comment":
            addError(lexeme, "Unmatched comment", lineCount)

        elif state == "COM_1_ACC":
            openComment = False

        elif state == "COM_2_ACC":
            openComment = False

        elif state == "unclosed_comment":
            openComment = False
            addError(lexeme, "Unclosed comment", startComment)

        elif state == "symbol_1":
            addToken("SYMBOL", lexeme, lineCount)

        elif state == "symbol_3":
            addToken("SYMBOL", lexeme, lineCount)

        elif state == "symbol_4_*":
            addToken("SYMBOL", lexeme[0: len(lexeme) - 1], lineCount)
            i -= 1

        elif state == "whitespace":
            if inputLine[i] == '\n':
                lineCount += 1

        else:
            flag = 1
            if state == "COM_2" or state == "COM_4":
                if not openComment:
                    startComment = lineCount
                openComment = True

        if flag == 0:
            break

    i += 1
