# Ali Sharifi 98109601
# Hamid Reza Dehbashi 98105762

class Node:
    idLen = 0
    nodes = []

    def __init__(self):
        self.id = Node.idLen
        Node.idLen += 1
        Node.nodes.append(self)
        self.start = None
        self.final = None
        self.to = {}
        self.to_ops = {}
        self.ops = []
        self.from_ops = {}


class NonTerminal:
    idLen = 0
    nonTerminals = []

    def __init__(self, name):
        self.name = name
        self.id = NonTerminal.idLen
        NonTerminal.idLen += 1
        NonTerminal.nonTerminals.append(self)
        self.start = None
        self.final = None
        self.first = []
        self.follow = []
        self.predict = []


def initialize_first():
    with open('first.txt', 'r') as file:
        frstTxt = file.readlines()

    terminals = frstTxt[0].split('\t')
    for i in range(len(terminals)):
        if terminals[i] == 'Îµ\n':
            terminals[i] = 'EPSILON'
    for i in range(1, len(frstTxt)):
        tempStr = frstTxt[i].split("\t")
        nontermName = tempStr[0]
        nonterm = getNonTermByName(nontermName)
        for j in range(1, len(tempStr)):
            if tempStr[j] == '+' or tempStr[j] == '+\n':
                nonterm.first.append(terminals[j - 1])


def initialize_follow():
    with open('follow.txt', 'r') as file:
        fllwTxt = file.readlines()

    terminals = fllwTxt[0].split('\t')
    for i in range(len(terminals)):
        if terminals[i] == 'â”¤\n':
            terminals[i] = '$'
    for i in range(1, len(fllwTxt)):
        tempStr = fllwTxt[i].split("\t")
        nontermName = tempStr[0]
        nonterm = getNonTermByName(nontermName)
        for j in range(1, len(tempStr)):
            if tempStr[j] == '+' or tempStr[j] == '+\n':
                nonterm.follow.append(terminals[j - 1])


def initialize_nodes():
    grmstr = ""
    with open('newGr3.txt', 'r') as file:
        grmstr = file.readlines()

    nodes = []
    nonTerminals = []
    nameToId = {}
    for i in range(0, len(grmstr)):
        grmstr[i] = grmstr[i][grmstr[i].index('.') + 2:]
        x = grmstr[i][:grmstr[i].index('>') - 2]
        nonterm = NonTerminal(x)
        nameToId.update({x: nonterm.id})
        nonTerminals.append(nonterm)
    for i in range(0, len(grmstr)):
        x = grmstr[i][:grmstr[i].index('>') - 2]
        if i != len(grmstr) - 1:
            y = grmstr[i][grmstr[i].index('>') + 2: len(grmstr[i]) - 1]
        else:
            y = grmstr[i][grmstr[i].index('>') + 2:]

        nonterm = getNonTermByName(x)
        startNode = Node()
        nodes.append(startNode)
        finalNode = Node()
        nodes.append(finalNode)
        startNode.start = nonterm
        finalNode.final = nonterm
        nonterm.start = startNode
        nonterm.final = finalNode
        rules_str = y
        rules = rules_str.split('|')
        for Rule in rules:
            dec = {}
            # gen = {}
            lastNode = startNode
            rule = Rule.split(" ")
            q = 0
            while q < len(rule):
                if rule[q] == '':
                    rule.pop(q)
                    q -= 1
                q += 1
            last_n_idx = 0
            for j in range(0, len(rule) + 1):
                if j == len(rule):
                    if last_n_idx not in dec:
                        dec[last_n_idx] = []
                    # if last_n_idx not in gen:
                    #    gen[last_n_idx] = []
                elif rule[j][0] == '#' or rule[j][0] == "%":
                    if last_n_idx not in dec:
                        dec[last_n_idx] = []
                    dec[last_n_idx].append(rule[j])
                # elif rule[j][0] == "%":
                #    if last_n_idx not in dec:
                #        dec[last_n_idx] = []
                #    dec[last_n_idx].append(rule[j])
                else:
                    if last_n_idx not in dec:
                        dec[last_n_idx] = []
                    # if last_n_idx not in gen:
                    #    gen[last_n_idx] = []
                    last_n_idx += 1
            tt = 0
            #print(dec[last_n_idx])
            while tt < len(rule):
                if rule[tt][0] == '#':
                    rule.pop(tt)
                elif rule[tt][0] == "%":
                    rule.pop(tt)
                else:
                    tt += 1
            #print(rule, dec)
            if len(rule) == 1:
                startNode.to.update({rule[0]: finalNode})
                startNode.to_ops.update({rule[0]: dec[0]})
                if dec[len(rule)] != []:
                    finalNode.from_ops[(startNode, rule[0])] = dec[len(rule)]
            else:
                if lastNode == startNode:
                    lastNode.to_ops.update({rule[0]: dec[0]})
                for j in range(0, len(rule) - 1):
                    temp = Node()
                    nodes.append(temp)
                    lastNode.to.update({rule[j]: temp})
                    if dec[j+1] != []:
                        temp.ops += dec[j+1]
                    lastNode = temp
                lastNode.to.update({rule[len(rule) - 1]: finalNode})
                #if dec[len(rule) - 1] != []:
                #    lastNode.ops += dec[len(rule) - 1]
                # if gen[len(rule) - 1] != []:
                #    lastNode.ops[1] += gen[len(rule) - 1]
                if dec[len(rule)] != []:
                    finalNode.from_ops[(lastNode, rule[len(rule) - 1])] = dec[len(rule)]
                # if gen[len(rule)] != []:
                #    finalNode.ops[1] += gen[len(rule)]

    #showNodes()


def showNodes():
    for nonTerm in NonTerminal.nonTerminals:
        start = nonTerm.start
        finish = nonTerm.final
        for x in start.to:
            y = start.to[x]
            print(start.id, start.to_ops[x], x, y.id)
            tt = x
            while True:
                if y == finish:
                    for t in y.from_ops:
                        if t[1] == tt:
                            print(y.from_ops[t])
                    print("......................")
                    break
                z = None
                for t in y.to:
                    z = y.to[t]
                    print(y.id, y.ops, t, z.id)
                    tt = t
                y = z


def getNonTermByName(name):
    for nonterm in NonTerminal.nonTerminals:
        if nonterm.name == name:
            return nonterm
    return None


###################################################################
table = {}  # DFA implementation table

# defining sets
digit = [i for i in '0123456789']
lowercase_letters = {chr(i) for i in range(ord('a'), ord('z') + 1)}
uppercase_letters = {i.upper() for i in lowercase_letters}
letter = lowercase_letters.union(uppercase_letters)
whitespace = {i for i in ' \n\r\t\v\f'}
symbol_except_eqStar = {i for i in ';:,[]()+-<{}'}

# Characters that are not result in "invalid_input" or "invalid_number" error after "id, number, =, *" states
after_id_acc = {';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<', '/'}
after_id_acc = after_id_acc.union(whitespace)
after_num_acc = {';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<', '/'}
after_num_acc = after_num_acc.union(whitespace)
after_eq_acc = {'/', '*'}
after_eq_acc = after_eq_acc.union(whitespace).union(letter).union(digit).union(symbol_except_eqStar)
after_star_acc = {'=', '*'}
after_star_acc = after_star_acc.union(whitespace).union(letter).union(digit).union(symbol_except_eqStar)

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

# state -> start
for i in letter:
    table['start'].update({i: 'ID_KEY'})
for i in digit:
    table['start'].update({i: 'NUM'})
for i in symbol_except_eqStar:
    table['start'].update({i: 'symbol_1'})
table['start'].update({'=': 'symbol_2'})
table['start'].update({'/': 'COM_1'})
for i in whitespace:
    table['start'].update({i: 'whitespace'})
table['start'].update({'*': 'V'})
table['start'].update({'other': 'invalid_input'})

# state -> ID_KEY
for i in letter.union(digit):
    table['ID_KEY'].update({i: 'ID_KEY'})
for i in after_id_acc:
    table['ID_KEY'].update({i: 'ID_KEY_ACC_*'})
table['ID_KEY'].update({'other': 'invalid_input'})
table['ID_KEY'].update({'EOF': 'ID_KEY_ACC'})

# state -> NUM
for i in digit:
    table['NUM'].update({i: 'NUM'})
for i in after_num_acc:
    table['NUM'].update({i: 'NUM_ACC_*'})
table['NUM'].update({'other': 'invalid_number'})
table['NUM'].update({'EOF': 'NUM_ACC'})

# state -> symbol_2
for i in after_eq_acc:
    table['symbol_2'].update({i: 'symbol_4_*'})
table['symbol_2'].update({'=': 'symbol_3'})
table['symbol_2'].update({'other': 'invalid_input'})
table['symbol_2'].update({'EOF': 'symbol_4'})

# state -> COM_1
table['COM_1'].update({'*': 'COM_2'})
table['COM_1'].update({'/': 'COM_4'})
for i in letter:
    table['COM_1'].update({i: 'invalid_input_*'})
for i in digit:
    table['COM_1'].update({i: 'invalid_input_*'})
for i in whitespace:
    table['COM_1'].update({i: 'invalid_input_*'})
for i in symbol_except_eqStar.union('='):
    table['COM_1'].update({i: 'invalid_input_*'})
table['COM_1'].update({'other': 'invalid_input'})
table['COM_1'].update({'EOF': 'invalid_input'})

# state -> COM_2
table['COM_2'].update({'other': 'COM_2'})
table['COM_2'].update({'*': 'COM_3'})
table['COM_2'].update({'EOF': 'unclosed_comment'})

# state -> COM_4
table['COM_4'].update({'other': 'COM_4'})
table['COM_4'].update({'\n': 'COM_2_ACC'})
table['COM_4'].update({'EOF': 'COM_2_ACC'})

# state -> COM_3
table['COM_3'].update({'other': 'COM_2'})
table['COM_3'].update({'/': 'COM_1_ACC'})
table['COM_3'].update({'EOF': 'unclosed_comment'})

# state -> V
for i in after_star_acc:
    table['V'].update({i: 'symbol_4_*'})
table['V'].update({'other': 'invalid_input'})
table['V'].update({'/': 'unmatched_comment'})
table['V'].update({'EOF': 'symbol_1'})
#####################################################################################

initialize_nodes()
initialize_first()
initialize_follow()
parse_table_txt = ""
syntax_error_txt = ""
traverse_list = [Node.nodes[0]]
middle_edge = '├── '
last_edge = '└── '
cont_edges = '│   '
space = '    '


def reformat(str):
    strLines = str.split("\n")
    strList = [list(x) for x in strLines]
    j = 0
    strList = strList[:-1]

    for i in range(len(strList) - 1, -1, -1):
        for j in range(len(strList[i])):
            if i == len(strList) - 1:
                if strList[i][j] == '│':
                    k = i
                    while k >= 0 and strList[k][j] == '│':
                        strList[k][j] = ' '
                        k -= 1
                    strList[k][j] = '└'
                elif strList[i][j] == '├':
                    strList[i][j] = '└'

            elif strList[i][j] == '│' and ((j < len(strList[i + 1]) and (
                    strList[i + 1][j] != '│' and strList[i + 1][j] != '├' and strList[i + 1][j] != '└')) or (
                                                   j >= len(strList[i + 1]))):
                k = i
                while k >= 0 and strList[k][j] == '│':
                    strList[k][j] = ' '
                    k -= 1
                strList[k][j] = '└'
            elif strList[i][j] == '├' and ((j < len(strList[i + 1]) and (
                    strList[i + 1][j] != '│' and strList[i + 1][j] != '├' and strList[i + 1][j] != '└')) or (
                                                   j >= len(strList[i + 1]))):
                strList[i][j] = '└'

    newList = [''.join(x) for x in strList]
    result = '\n'.join(newList)
    return result


def write_file_parser():
    global parse_table_txt, syntax_error_txt
    parse_table_txt = reformat(parse_table_txt)
    with open('parse_tree.txt', mode='w', encoding="utf-8") as f:
        f.write(parse_table_txt)
    if len(syntax_error_txt) == 0:
        syntax_error_txt = "There is no syntax error."
    with open('syntax_errors.txt', mode='w', encoding="utf-8") as e:
        e.write(syntax_error_txt.replace('_', '-'))


def write_epsilon(node_, edge_type_):
    global parse_table_txt, traverse_list
    parse_table_txt += calc_line_first_part() + edge_type_ + 'epsilon' + '\n'
    traverse_list.append(node_)


def write_term(node_, la_role_, la_tok_, edge_type_):
    global parse_table_txt, traverse_list
    if la_role_ == "$" and la_tok_ == "$":
        parse_table_txt += calc_line_first_part() + edge_type_ + "$" + '\n'
    else:
        parse_table_txt += calc_line_first_part() + edge_type_ + '(' + la_role_ + ', ' + la_tok_ + ')' + '\n'
    traverse_list.append(node_)


def write_nonterm(node_, res_, edge_type_):
    global parse_table_txt, traverse_list
    resName = res_.name.replace('_', '-')
    parse_table_txt += calc_line_first_part() + edge_type_ + resName + '\n'
    traverse_list.append(node_)
    traverse_list.append(res_.start)


def calc_line_first_part():
    line_first_part = ''
    for node in traverse_list:
        if node.final:
            line_first_part += space
        else:
            line_first_part += cont_edges
    return line_first_part


def initSymbolTable(keywords):
    """
    Puts keywords on the beginning of the symbol table
    """
    for xX in keywords:
        symbolTable.update({xX: len(symbolTable) + 1})


def addToken(token, lexeme_temp, line):
    """
    Gets a token and puts its lexeme on the corresponding line in the tokens table
    """
    if line not in tokens:
        tokens.update({line: []})
    tokens[line].append((token, lexeme_temp))


def addError(lexeme_temp, error, line):
    """
    Gets an error and puts its lexeme on the corresponding line in the error table
    """
    if line not in errors:
        errors.update({line: []})
    errors[line].append((lexeme_temp, error))


def addSymbolTable(lexeme_temp):
    """
    Gets an id and puts it on the corresponding line in the symbol table
    """
    if lexeme_temp not in symbolTable:
        symbolTable.update({lexeme_temp: len(symbolTable) + 1})


def write_file_lexical():
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
            errorTxt += "(" + str(x[0]).strip('"\'') + ", " + str(x[1]).strip('"\'') + ")" + " "
        errorTxt += "\n"
    if len(errors) == 0:
        errorTxt = "There is no lexical error."

    # Write in file
    with open("lexical_errors.txt", "w") as lexical:
        lexical.write(errorTxt)

    with open("tokens.txt", "w") as tokenFile:
        tokenFile.write(tokenTxt)

    with open("symbol_table.txt", "w") as symbolFile:
        symbolFile.write(symbolTxt)


def get_next_token_parser():
    result = get_next_token()
    while result == '' or result == None:
        result = get_next_token()
    # print(result)
    return result


def get_next_token():
    ret = ''
    global i, lineCount, openComment, startComment
    if i >= len(inputLine):
        return '$', '$'
    while i < len(inputLine):
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
                    ret = ('KEYWORD', lexeme)
                else:
                    addToken("ID", lexeme, lineCount)
                    ret = ('ID', lexeme)
                    addSymbolTable(lexeme)
                i -= 1

            elif state == "ID_KEY_ACC":
                if lexeme in keywords:
                    addToken("KEYWORD", lexeme, lineCount)
                    ret = ('KEYWORD', lexeme)
                else:
                    addToken("ID", lexeme, lineCount)
                    ret = ('ID', lexeme)
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
                ret = ('NUM', lexeme[0:len(lexeme) - 1])
                i -= 1

            elif state == "NUM_ACC":
                addToken("NUM", lexeme, lineCount)
                ret = ('NUM', lexeme)

            elif state == "unmatched_comment":
                addError(lexeme, "Unmatched comment", lineCount)

            elif state == "COM_1_ACC":
                openComment = False

            elif state == "COM_2_ACC":
                openComment = False

            elif state == "unclosed_comment":
                openComment = False
                if len(lexeme) > 7:
                    lexeme = lexeme[0:7] + "..."
                addError(lexeme, "Unclosed comment", startComment)

            elif state == "symbol_1":
                addToken("SYMBOL", lexeme, lineCount)
                ret = ('SYMBOL', lexeme)

            elif state == "symbol_3":
                addToken("SYMBOL", lexeme, lineCount)
                ret = ('SYMBOL', lexeme)

            elif state == "symbol_4_*":
                if inputLine[i] == '\n':
                    lineCount -= 1
                addToken("SYMBOL", lexeme[0: len(lexeme) - 1], lineCount)
                ret = ('SYMBOL', lexeme[0:len(lexeme) - 1])
                i -= 1

            elif state == "symbol_4":
                addToken("SYMBOL", lexeme, lineCount)
                ret = ('SYMBOL', lexeme)

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
        return ret


stack = []
symbTable = []
lastSymbElem = None
curAddrCode = 0
curAddrData = 500
curAddrTemp = 1000
curScope = 0
breakPoints = []
genCode = []

for i in range(100000):
    genCode.append("")


def getTemp():
    global curAddrTemp
    curAddrTemp += 4
    return curAddrTemp - 4


def findLastFuncSymbol():
    for i in range(len(symbTable) - 1, -1, -1):
        if symbTable[i]['FuncArrVar'] == 'Func':
            return i
    return -1

def getIdxByAddr(a):
    for i in range(len(symbTable) - 1, -1, -1):
        if symbTable[i]['Address'] == a:
            return i
    return -1


def findAddrSymb(inp):
    for i in range(len(symbTable) - 1, -1, -1):
        if symbTable[i]['Lexeme'] == inp:
            return i
    return -1


def codeGen(action, input):
    print(action, input)
    print("stack:", stack)
    global lastSymbElem, curAddrCode, curAddrTemp, curAddrData, curScope
    if action == '%defAddr':
        if lastSymbElem is None:
            lastSymbElem = {'Address': curAddrData, 'Type': None, 'Lexeme': None, 'FuncArrVar': None, 'Scope': None,
                            'CodeAddress': None}
            symbTable.append(lastSymbElem)
        else:
            if lastSymbElem['Address'] is not None:
                lastSymbElem = {'Address': curAddrData, 'Type': None, 'Lexeme': None, 'FuncArrVar': None, 'Scope': None,
                                'CodeAddress': None}
                symbTable.append(lastSymbElem)
            else:
                lastSymbElem['Address'] = curAddrData
                symbTable[len(symbTable) - 1] = lastSymbElem
    elif action == '%defScope':
        lastSymbElem['Scope'] = curScope
        symbTable[len(symbTable) - 1] = lastSymbElem
    elif action == '%defType':
        lastSymbElem['Type'] = input
        symbTable[len(symbTable) - 1] = lastSymbElem
    elif action == '%defLex':
        lastSymbElem['Lexeme'] = input
        symbTable[len(symbTable) - 1] = lastSymbElem
    elif action == '%updateAddr1':
        curAddrData += 4
    # elif action == '%args1':
    #
    elif action == '%varSpec':
        lastSymbElem['FuncArrVar'] = 'Var'
        symbTable[len(symbTable) - 1] = lastSymbElem
    elif action == '%updateAddr2':
        curAddrData += int(input)
    # elif action == '%args2':
    #
    elif action == '%arrSpec':
        lastSymbElem['FuncArrVar'] = 'Arr'
        symbTable[len(symbTable) - 1] = lastSymbElem
    elif action == '%funcSpec':
        lastSymbElem['FuncArrVar'] = 'Func'
        symbTable[len(symbTable) - 1] = lastSymbElem
    elif action == '%returnAddrVal':
        curAddrData += 12
    elif action == '%codeAddr':
        lastSymbElem['CodeAddress'] = curAddrCode
        symbTable[len(symbTable) - 1] = lastSymbElem
    elif action == '%arrPointerSpec':
        lastSymbElem['Type'] += "*"
        symbTable[len(symbTable) - 1] = lastSymbElem
    elif action == '%updateScopeInc':
        curScope += 1
    elif action == '%updateScopeDec':
        curScope -= 1

    elif action == '#breakPoint':
        breakPoints.append(curAddrCode + 1)
        code = "(JP, " + str(curAddrCode + 2) + ", , )"
        genCode[curAddrCode] = code
        curAddrCode += 2

    elif action == '#jumpToEnd':
        code = "(JP, " + str(breakPoints[-1]) + ", , )"
        genCode[curAddrCode] = code
        curAddrCode += 1

    elif action == '#saveIf':
        stack.append(curAddrCode)
        curAddrCode += 1

    elif action == '#jif':
        code = "(JPF, " + str(int(stack[len(stack) - 2])) + ", " + str(curAddrCode + 1) + ", )"
        genCode[int(stack[len(stack) - 1])] = code
        stack.pop()
        stack.pop()
        stack.append(curAddrCode)
        curAddrCode += 1

    elif action == '#jp':
        code = "(JP, " + str(curAddrCode) + ", , )"
        genCode[int(stack[len(stack) - 1])] = code
        stack.pop()

    elif action == '#jpf':
        code = "(JPF, " + str(int(stack[len(stack) - 2])) + ", " + str(curAddrCode) + ", )"
        genCode[int(stack[len(stack) - 1])] = code
        stack.pop()
        stack.pop()

    elif action == '#li':
        stack.append(curAddrCode)

    elif action == '#ji':
        code = "(JPF, " + str(int(stack[len(stack) - 1])) + ", " + str(int(stack[len(stack) - 2])) + ", )"
        genCode[curAddrCode] = code
        curAddrCode += 1
        stack.pop()
        stack.pop()

    elif action == '#eoi':
        code = "(JP, " + str(curAddrCode) + ", , )"
        genCode[breakPoints[-1]] = code
        breakPoints.pop()

    elif action == '#jr':
        returnAddr = symbTable[findLastFuncSymbol()]['Address'] + 4
        code = "(JP, " + str(returnAddr) + ", , )"
        genCode[curAddrCode] = code
        curAddrCode += 1

    elif action == '#assR':
        returnVal = symbTable[findLastFuncSymbol()]['Address'] + 8
        code = '(ASSIGN, ' + str(stack[-1]) + ", " + str(returnVal) + ', )'
        stack.pop()
        genCode[curAddrCode] = code
        curAddrCode += 1

    elif action == '#pidAddr':
        p = symbTable[findAddrSymb(input)]['Address']
        stack.append(p)

    # elif action == '#readAddr':
    #
    #
    elif action == '#assign':
        code = '(ASSIGN, ' + str(stack[-1]) + ", " + str(stack[-2]) + ', )'
        stack.pop()
        stack.pop()
        genCode[curAddrCode] = code
        curAddrCode += 1


    elif action == '#arrIdx':
        temp = getTemp()
        if symbTable[getIdxByAddr(stack[-1])]["Type"][-1] == "*":
            code = "(ADD, @" + str(stack[-1]) + ", " + '#' + str(stack[-2]) + ", " + str(temp) + ")"
        else:
            code = "(ADD, " + str(stack[-1]) + ", " + '#' + str(stack[-2]) + ", " + str(temp) + ")"
        genCode[curAddrCode] = code
        stack.pop()
        stack.pop()
        stack.append(temp)
        curAddrCode += 1

    elif action == '#compare':
        temp = getTemp()
        if stack[-2] == '<':
            code = "(LT, " + str(stack[-3]) + ", " + str(stack[-1]) + ", " + str(temp) + ")"
        elif stack[-2] == '==':
            code = "(EQ, " + str(stack[-3]) + ", " + str(stack[-1]) + ", " + str(temp) + ")"
        genCode[curAddrCode] = code
        curAddrCode += 1
        stack.pop()
        stack.pop()
        stack.append(temp)
    elif action == '#mult':
        temp = getTemp()
        code = '(MULT, ' + str(stack[-1]) + ', ' + str(stack[-2]) + ', ' + str(temp) + ')'
        genCode[curAddrCode] = code
        curAddrCode += 1
        stack.pop()
        stack.pop()
        stack.append(temp)
    elif action == '#addMinus':
        temp = getTemp()
        code = ""
        if stack[-2] == '+':
            code = "(ADD, " + str(stack[-1]) + ", " + str(stack[-3]) + ", " + str(temp) + ")"
        elif stack[-2] == '-':
            code = "(SUB, " + str(stack[-3]) + ", " + str(stack[-1]) + ", " + str(temp) + ")"
        genCode[curAddrCode] = code
        curAddrCode += 1
        stack.pop()
        stack.pop()
        stack.append(temp)
    elif action == '#pushLess':
        stack.append('<')

    elif action == '#pushEq':
        stack.append('==')

    elif action == '#pushPlus':
        stack.append('+')

    elif action == '#pushMinus':
        stack.append('-')

    elif action == '#pushNum':
        temp = getTemp()
        code = '(ASSIGN, #' + input + ", " + str(temp) + ', )'
        genCode[curAddrCode] = code
        curAddrCode += 1
        stack.append(temp)

    elif action == '#jf':
        returnAddr = stack[-1] + 4
        code = '(ASSIGN, ' + str(curAddrCode + 2) + ", " + str(returnAddr) + ', )'
        genCode[curAddrCode] = code
        curAddrCode += 1

        codeAddr = symbTable[getIdxByAddr(stack[-1])]['CodeAddress']
        code = "(JP, " + str(codeAddr) + ", , )"
        genCode[curAddrCode] = code
        curAddrCode += 1

    elif action == '#pushReturn':
        returnVal = stack[-1] + 8
        stack.pop()
        stack.append(returnVal)

    elif action == '#specDataAddrFunc':
        stack.append(stack[-1] + 12)

    elif action == '#pushAgain':
        stack.append(stack[-1])

    elif action == '#updateNextArgAddr':
        stack[-1] = stack[-1] + 4

    elif action == '#popAgain':
        stack.pop()


# Auxiliary variables
lineCount = 1
state = ""
tokens = {}
errors = {}
symbolTable = {}
keywords = ["if", "else", "void", "int", "repeat", "break", "until", "return", "endif"]
openComment = False
startComment = -1
initSymbolTable(keywords)

f = open('input.txt', 'r')
inputLine = f.read()
i = 0
flag_exit = 0
last_la_tok = ""
la_role, la_tok = get_next_token_parser()
parse_table_txt += 'Program\n'
while traverse_list and not flag_exit:
    match = False
    print(last_la_tok)
    last_node = traverse_list.pop()
    if last_node.final:
        continue
    for term_nonterm, node in last_node.to.items():
        res = getNonTermByName(term_nonterm)
        edge_type = last_edge if node.final else middle_edge
        if res:
            if la_role == 'NUM' or la_role == 'ID':
                if la_role in res.first:
                    write_nonterm(node, res, edge_type)
                    match = True
                    break
                elif 'EPSILON' in res.first and la_role in res.follow:
                    write_nonterm(node, res, edge_type)
                    match = True
                    break
            else:
                if la_tok in res.first:
                    write_nonterm(node, res, edge_type)
                    match = True
                    break
                elif 'EPSILON' in res.first and la_tok in res.follow:
                    write_nonterm(node, res, edge_type)
                    match = True
                    break
        else:
            if la_role == 'NUM' or la_role == 'ID':
                if la_role == term_nonterm:
                    write_term(node, la_role, la_tok, edge_type)
                    last_la_tok = la_tok
                    la_role, la_tok = get_next_token_parser()
                    match = True
                    break
                elif term_nonterm == 'EPSILON' and la_role in node.final.follow:
                    write_epsilon(node, edge_type, )
                    match = True
                    break
            else:
                if la_tok == term_nonterm:
                    write_term(node, la_role, la_tok, edge_type)
                    last_la_tok = la_tok
                    la_role, la_tok = get_next_token_parser()
                    match = True
                    break
                elif term_nonterm == 'EPSILON' and la_tok in node.final.follow:
                    write_epsilon(node, edge_type)
                    match = True
                    break
    if match:
        if term_nonterm in last_node.to_ops:
            for x in last_node.to_ops[term_nonterm]:
                codeGen(x, last_la_tok)
        elif term_nonterm in last_node.from_ops:
            for x in last_node.from_ops[term_nonterm]:
                codeGen(x, last_la_tok)
        elif last_node.ops != []:
            for x in last_node.ops:
                codeGen(x, last_la_tok)

        match = False
    else:
        if la_tok == "$":
            syntax_error_txt += f'#{lineCount} : syntax error, Unexpected EOF'
            flag_exit = True
            break
        flag, err_name = False, None
        for term_nonterm, node in last_node.to.items():
            res = getNonTermByName(term_nonterm)
            if res:
                if la_role == 'NUM' or la_role == 'ID':
                    if la_role in res.follow:
                        syntax_error_txt += f'#{lineCount} : syntax error, missing {term_nonterm}\n'
                        traverse_list.append(node)
                        flag = True
                        err_name = term_nonterm
                        break
                else:
                    if la_tok in res.follow:
                        syntax_error_txt += f'#{lineCount} : syntax error, missing {term_nonterm}\n'
                        traverse_list.append(node)
                        flag = True
                        break
            else:
                if len(last_node.to) == 1:
                    syntax_error_txt += f'#{lineCount} : syntax error, missing {term_nonterm}\n'
                    traverse_list.append(node)
                    flag = True
                    break
        if not flag and not flag_exit:
            syntax_error_txt += f'#{lineCount} : syntax error, illegal {la_role if la_role == "ID" or la_role == "NUM" else la_tok}\n'
            traverse_list.append(last_node)
            la_role, la_tok = get_next_token_parser()
            flag = False

write_file_lexical()
write_file_parser()
