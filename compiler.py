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
        state = (table[state])[inputLine[i]]
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
