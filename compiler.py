def addToken(token, lexeme_temp, line):
    if line not in tokens:
        tokens.update({line: []})
    tokens[line].append((token, lexeme_temp))


def addError(lexeme_temp, error, line):
    if line not in errors:
        errors.update({line: []})
    errors[line].append((lexeme_temp, error))


def addSymbolTable(lexeme_temp):
    if not lexeme_temp in symbolTable:
        symbolTable.update({lexeme_temp: len(symbolTable) + 1})


def initSymbolTable():
    for x in keywords:
        symbolTable.update({x: len(symbolTable) + 1})


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
letter = lowercase_letters.union(uppercase_letters)
whitespace = {i for i in ' \n\r\t\v\f'}
symbol_except_eq = {i for i in ';:,[]()+-<{}'}

#TODO
after_id_acc = {' ', '=', '<', '(', ')', '{', '}', '[', ']', ';', ':', '+', '-', '*', ','}  # TODO complete
after_id_acc = after_id_acc.union(whitespace)
after_num_acc = {' ', '=', '<', '(', ')', '{', '}', '[', ']', ';', ':', '+', '-', '*', ','}  # TODO complete
after_num_acc = after_num_acc.union(whitespace)
after_eq_acc = {'('}
after_eq_acc = after_eq_acc.union(whitespace).union(letter).union(digit)
after_star_acc = after_eq_acc

#alphabet = {chr(i) for i in range(32, 127)} + whitespace + ''  # all printable ASCIIs
# TODO defining others!
#start_other = {}
#ID_KEY_other = {}
#NUM_other = {}

# initializing table
table.update({'start': {}})

table.update({'ID_KEY': {}})
table.update({'ID_KEY_ACC_*': {}})

table.update({'invalid_input': {}})
table.update({'invalid_input_*': {}})
table.update({'invalid_number': {}})
table.update({'unmatched_comment': {}})
table.update({'unclosed_comment': {}})

table.update({'NUM': {}})
table.update({'NUM_ACC_*': {}})

table.update({'symbol_1': {}})
table.update({'symbol_2': {}})
table.update({'symbol_3': {}})
table.update({'symbol_4_*': {}})

table.update({'COM_1': {}})
table.update({'COM_2': {}})
table.update({'COM_3': {}})
table.update({'COM_4': {}})
table.update({'COM_1_ACC': {}})
table.update({'COM_2_ACC': {}})

table.update({'whitespace': {}})

table.update({'V': {}})

for i in letter:
    table['start'].update({i: 'ID_KEY'})
for i in digit:
    table['start'].update({i: 'NUM'})
for i in symbol_except_eq:
    table['start'].update({i: 'symbol_1'})
table['start'].update({'=': 'symbol_2'})
table['start'].update({'/': 'COM_1'})
for i in whitespace:
    table['start'].update({i: 'whitespace'})
table['start'].update({'*': 'V'})
#table['start'].update({'EOF': 'END'})
table['start'].update({'other': 'invalid_input'})

for i in letter.union(digit):
    table['ID_KEY'].update({i: 'ID_KEY'})
for i in after_id_acc:
    table['ID_KEY'].update({i: 'ID_KEY_ACC_*'})
table['ID_KEY'].update({'other': 'invalid_input'})
table['ID_KEY'].update({'EOF': 'ID_KEY_ACC'})

# for i in ID_KEY_other:
#    table['ID_KEY'].update({i: 'invalid_input'})

for i in digit:
    table['NUM'].update({i: 'NUM'})
for i in after_num_acc:
    table['NUM'].update({i: 'NUM_ACC_*'})
table['NUM'].update({'other': 'invalid_number'})
table['NUM'].update({'EOF': 'NUM_ACC'})

# for i in NUM_other:
#    table['NUM'].update({i: 'invalid_number'})

for i in after_eq_acc:
    table['symbol_2'].update({i: 'symbol_4_*'})
table['symbol_2'].update({'=': 'symbol_3'})
table['symbol_2'].update({'other': 'invalid_input'})
table['symbol_2'].update({'EOF': 'symbol_4'})

# for i in alphabet - {'='}:
#    table['symbol_2'].update({i: 'symbol_4_*'})

# for i in alphabet - {'/', '*'}:
#    table['COM_1'].update({i: 'invalid_input_*'})
table['COM_1'].update({'*': 'COM_2'})
table['COM_1'].update({'/': 'COM_4'})
table['COM_1'].update({'other': 'invalid_input_*'})
table['COM_1'].update({'EOF': 'invalid_input'})


# for i in alphabet - {'', '*'}:
#    table['COM_2'].update({i: 'COM_2'})
table['COM_2'].update({'other': 'COM_2'})
table['COM_2'].update({'*': 'COM_3'})
table['COM_2'].update({'EOF': 'unclosed_comment'})


# for i in alphabet - {'', '\n'}:
#    table['COM_4'].update({i: 'COM_4'})
table['COM_4'].update({'other': 'COM_4'})
table['COM_4'].update({'': 'COM_2_ACC'})
table['COM_4'].update({'\n': 'COM_2_ACC'})
table['COM_4'].update({'EOF': 'COM_2_ACC'})


# for i in alphabet - {'', '/'}:
#    table['COM_3'].update({i: 'COM_2'})
table['COM_3'].update({'other': 'COM_2'})
table['COM_3'].update({'': 'unclosed_comment'})
table['COM_3'].update({'/': 'COM_1_ACC'})
table['COM_3'].update({'EOF': 'unclosed_comment'})

# for i in alphabet - {'/'}:
#    table['V'].update({i: 'invalid_input_*'})
for i in after_star_acc:
    table['V'].update({i: 'symbol_4_*'})
table['V'].update({'other': 'invalid_input'})
table['V'].update({'/': 'unmatched_comment'})
table['V'].update({'EOF': 'symbol_1'})

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

while getNextToken and i < len(inputLine):
    lexeme = ""
    state = "start"
    while True:
        if i < len(inputLine) and inputLine[i] in table[state]:
            state = (table[state])[inputLine[i]]
            lexeme += inputLine[i]
            if inputLine[i] == '\n':
                lineCount += 1
            temp = 0
        elif i == len(inputLine):
            state = (table[state])["EOF"]
        else:
            state = (table[state])["other"]
            lexeme += inputLine[i]
            if inputLine[i] == '\n':
                lineCount += 1

        flag = 0
        if state == "ID_KEY_ACC_*":
            if inputLine[i] == '\n':
                lineCount -= 1
            lexeme = lexeme[0: len(lexeme) - 1]
            if lexeme in keywords:
                addToken("KEYWORD", lexeme, lineCount)
            else:
                addToken("ID", lexeme, lineCount)
                addSymbolTable(lexeme)
            i -= 1


        elif state == "ID_KEY_ACC":
            if lexeme in keywords:
                addToken("KEYWORD", lexeme, lineCount)
            else:
                addToken("ID", lexeme, lineCount)
                addSymbolTable(lexeme)

        elif state == "invalid_input":
            addError(lexeme, "Invalid input", lineCount)

        elif state == "invalid_input_*":
            if inputLine[i] == '\n':
                lineCount -= 1
            addError(lexeme[0: len(lexeme) - 1], "Invalid input", lineCount)
            i -= 1

        elif state == "invalid_number":
            addError(lexeme, "Invalid number", lineCount)

        elif state == "NUM_ACC_*":
            if inputLine[i] == '\n':
                lineCount -= 1
            addToken("NUM", lexeme[0: len(lexeme) - 1], lineCount)
            i -= 1

        elif state == "NUM_ACC":
            addToken("NUM", lexeme, lineCount)

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
            if inputLine[i] == '\n':
                lineCount -= 1
            addToken("SYMBOL", lexeme[0: len(lexeme) - 1], lineCount)
            i -= 1

        elif state == "symbol_4":
            addToken("SYMBOL", lexeme, lineCount)

        elif state == "whitespace":
            temp = 0

        else:
            flag = 1
            if state == "COM_2" or state == "COM_4":
                if not openComment:
                    startComment = lineCount
                openComment = True

        i += 1

        if flag == 0:
            break


tokenTxt = ""
for i in tokens:
    tokenTxt += str(i).strip('"\'') + ".	"
    for x in tokens[i]:
        tokenTxt += "(" + str(x[0]).strip('"\'') + ", " + str(x[1]).strip('"\'') + ")" + " "
    tokenTxt += "\n"

symbolTxt = ""
for i in symbolTable:
    symbolTxt += str(symbolTable[i]).strip('"\'') + ".	" + str(i).strip('"\'')
    symbolTxt += "\n"

errorTxt = ""
for i in errors:
    errorTxt += str(i).strip('"\'') + ".	"
    for x in errors[i]:
        if x[1] == 'Unclosed comment':
            errorTxt += '(' + (str(x[0][:7]) + '...').strip('"\'') + ", " + str(x[1]).strip('"\'') + ")" + " "
        else:
            errorTxt += "(" + str(x[0]).strip('"\'') + ", " + str(x[1]).strip('"\'') + ")" + " "
    errorTxt += "\n"
if len(errors) == 0:
    errorTxt = "There is no lexical error."

with open("lexical_errors.txt", "w") as lexical:
    lexical.write(errorTxt)

with open("tokens.txt", "w") as tokenFile:
    tokenFile.write(tokenTxt)

with open("symbol_table.txt", "w") as symbFile:
    symbFile.write(symbolTxt)
