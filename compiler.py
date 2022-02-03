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
        if terminals[i] == 'ε\n':
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
        if terminals[i] == '┤\n':
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
                elif rule[j][0] == '#' or rule[j][0] == "%" or rule[j][0] == "@":
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
            #print(dec)
            while tt < len(rule):
                if rule[tt][0] == '#':
                    rule.pop(tt)
                elif rule[tt][0] == "%" or rule[tt][0] == "@":
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
            past_y = start
            y = start.to[x]
            print(start.id, start.to_ops[x], x, y.id)
            tt = x
            while True:
                if y == finish:
                    for t in y.from_ops:
                        if t[1] == tt and t[0] == past_y:
                            print(y.from_ops[t])
                    print("......................")
                    break
                z = None
                for t in y.to:
                    z = y.to[t]
                    print(y.id, y.ops, t, z.id)
                    tt = t
                past_y = y
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
semantic_errors = []
semantic_errors_shdw = []
traverse_list = [Node.nodes[0]]
shadow = [False]
nonTermShadow = [""]
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
    shadow.append(False)
    nonTermShadow.append("")
    traverse_list.append(node_)


def write_term(node_, la_role_, la_tok_, edge_type_):
    global parse_table_txt, traverse_list
    if la_role_ == "$" and la_tok_ == "$":
        parse_table_txt += calc_line_first_part() + edge_type_ + "$" + '\n'
    else:
        parse_table_txt += calc_line_first_part() + edge_type_ + '(' + la_role_ + ', ' + la_tok_ + ')' + '\n'
    shadow.append(False)
    nonTermShadow.append("")
    traverse_list.append(node_)


def write_nonterm(node_, res_, edge_type_):
    global parse_table_txt, traverse_list
    resName = res_.name.replace('_', '-')
    parse_table_txt += calc_line_first_part() + edge_type_ + resName + '\n'
    shadow.append(False)
    nonTermShadow.append("")
    shadow.append(False)
    nonTermShadow.append("")
    traverse_list.append(node_)
    traverse_list.append(res_.start)


def calc_line_first_part():
    line_first_part = ''
    for i in range(len(traverse_list)):
        if shadow[i] == True:
            continue
        node = traverse_list[i]
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

argsStack = []
stackFuncScope = []
stack = []
symbTable = []
lastSymbElem = None
curAddrCode = 3
curAddrData = 500
curAddrTemp = 1000
curScope = 0
breakPoints = []
genCode = []
semanticStack = []
funcArgsCountStack = []
overall_errors = []

for i in range(500):
    genCode.append("")

genCode[1] = "(PRINT, 512, , )"
genCode[2] = "(JP, @504, , )"


def write_symb_table():
    st = ""
    for x in symbTable:
        for y in x.keys():
            st += str(x[y]) + '\t'
        st += '\n'
    st = st[:-1]
    with open('Main_Symbol_Table.txt', 'w') as g:
        g.write(st)


def getTemp():
    global curAddrTemp
    curAddrTemp += 4
    return curAddrTemp - 4


def findLastFuncSymbol():
    for i in range(len(symbTable) - 1, -1, -1):
        if symbTable[i]['FuncArrVar'] == 'Func':
            return i
    return -1


def findLastFuncSymbolScope(sc):
    temp = sc
    for i in range(len(symbTable) - 1, -1, -1):
        if symbTable[i]["Scope"] > temp:
            continue
        if symbTable[i]["Scope"] < temp:
            temp = symbTable[i]["Scope"]
        if symbTable[i]['FuncArrVar'] == 'Func' and temp >= symbTable[i]["Scope"]:
            return i
    return -1


def getIdxByAddr(a):
    for i in range(len(symbTable) - 1, -1, -1):
        if symbTable[i]['Address'] == a:
            return i
    return -1


def findFuncLex(w, sc):
    temp = sc
    for i in range(len(symbTable) - 1, -1, -1):
        if symbTable[i]["Scope"] > temp:
            continue
        if symbTable[i]["Scope"] < temp:
            temp = symbTable[i]["Scope"]
        if symbTable[i]['FuncArrVar'] == 'Func' and temp >= symbTable[i]["Scope"] and w == symbTable[i]["Lexeme"]:
            return i
    return -1


def findArrLex(w, sc):
    temp = sc
    for i in range(len(symbTable) - 1, -1, -1):
        if symbTable[i]["Scope"] > temp:
            continue
        if symbTable[i]["Scope"] < temp:
            temp = symbTable[i]["Scope"]
        if (symbTable[i]['FuncArrVar'] == 'Arr' or symbTable[i]['Type'] == 'int*') and temp >= symbTable[i]["Scope"] and w == symbTable[i]["Lexeme"]:
            return i
    return -1


def findLex(w, sc):
    temp = sc
    for i in range(len(symbTable) - 1, -1, -1):
        if symbTable[i]["Scope"] > temp:
            continue
        if symbTable[i]["Scope"] < temp:
            temp = symbTable[i]["Scope"]
        if temp >= symbTable[i]["Scope"] and w == symbTable[i]["Lexeme"]:
            return i
    return -1


def findAddrSymb(inp):
    for i in range(len(symbTable) - 1, -1, -1):
        if symbTable[i]['Lexeme'] == inp:
            return i
    return -1


def write_semantic_errors():
    sqq = ""
    for line in semantic_errors:
       sqq += line + '\n'
    #sqq = sqq[:-1]

    with open('semantic_errors.txt', 'w') as y:
        if semantic_errors == []:
            y.write("The input program is semantically correct")
        else:
            y.write(sqq)


def chk(line, lex):
    """for l, x in overall_errors:
        if line == l and x == lex:
            return False"""
    return True


def write_generated_code():
    finalCode = ""
    count = 0
    genCode[0] = "(JP, " + str(symbTable[findAddrSymb("main")]['CodeAddress']) + ", , )"
    for line in genCode:
        if line != "":
            finalCode += str(count) + '\t' + line + '\n'
            count += 1
    finalCode = finalCode[:-1]
    with open("output.txt", "w") as gen_code:
        if semantic_errors == []:
            gen_code.write(finalCode)
        else:
            gen_code.write("The code has not been generated.")

def codeGen(action, input):
    print(lineCount - 2, action, input)
    print("stack:", stack)
    print("semantic_stack:", semanticStack)
    print("semantic_errors:", semantic_errors)
    print(".......................................................")
    global lastSymbElem, curAddrCode, curAddrTemp, curAddrData, curScope
    if action == '%defAddr':
        if lastSymbElem is None:
            lastSymbElem = {'Address': curAddrData, 'Type': None, 'Lexeme': None, 'FuncArrVar': None, 'Scope': None,
                            'CodeAddress': None, 'No.Args': 0}
            symbTable.append(lastSymbElem)
        else:
            if lastSymbElem['Address'] is not None:
                lastSymbElem = {'Address': curAddrData, 'Type': None, 'Lexeme': None, 'FuncArrVar': None, 'Scope': None,
                                'CodeAddress': None, 'No.Args': 0}
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
        curAddrData += int(input) * 4
    # elif action == '%args2':
    #
    elif action == '%arrSpec':
        lastSymbElem['FuncArrVar'] = 'Arr'
        symbTable[len(symbTable) - 1] = lastSymbElem
    elif action == '%funcSpec':
        stackFuncScope.append(len(stack))
        lastSymbElem['FuncArrVar'] = 'Func'
        symbTable[len(symbTable) - 1] = lastSymbElem
    elif action == '%returnAddrVal':
        curAddrData += 12
    elif action == '%codeAddr':
        lastSymbElem['CodeAddress'] = curAddrCode
        symbTable[len(symbTable) - 1] = lastSymbElem
        symbTable[0]['CodeAddress'] = 1
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
        #print("breakPoints:", breakPoints)
        if len(breakPoints) > 0:
            code = "(JP, " + str(breakPoints[-1]) + ", , )"
            genCode[curAddrCode] = code
            curAddrCode += 1

    elif action == '#saveIf':
        stack.append(curAddrCode)
        curAddrCode += 1

    elif action == '#jif':
        if len(stack) > 1:
            code = "(JPF, " + str(stack[len(stack) - 2]) + ", " + str(curAddrCode + 1) + ", )"
            genCode[int(stack[len(stack) - 1])] = code
            stack.pop()
            stack.pop()
            stack.append(curAddrCode)
            curAddrCode += 1

    elif action == '#jp':
        if len(stack) > 0:
            code = "(JP, " + str(curAddrCode) + ", , )"
            genCode[int(stack[len(stack) - 1])] = code
            stack.pop()

    elif action == '#jpf':
        if len(stack) > 1:
            code = "(JPF, " + str(int(stack[len(stack) - 2])) + ", " + str(curAddrCode) + ", )"
            genCode[int(stack[len(stack) - 1])] = code
            stack.pop()
            stack.pop()

    elif action == '#li':
        stack.append(curAddrCode)

    elif action == '#ji':
        #code = "(JPF, " + str(int(stack[len(stack) - 1])) + ", " + str(curAddrCode + 2) + ", )"
        #genCode[curAddrCode] = code
        #curAddrCode += 1
        #code = "(JP, " + str(int(stack[len(stack) - 2])) + ", , )"
        if len(stack) > 1:
            code = "(JPF, " + str(int(stack[-1])) + ", " + str(int(stack[-2])) + ", )"
            genCode[curAddrCode] = code
            curAddrCode += 1
            stack.pop()
            stack.pop()

    elif action == '#eoi':
        if len(breakPoints) > 0:
            code = "(JP, " + str(curAddrCode) + ", , )"
            genCode[breakPoints[-1]] = code
            breakPoints.pop()

    elif action == '#jumpBack':
        if symbTable[findLastFuncSymbolScope(curScope)]["Lexeme"] != 'main':
            returnAddr = symbTable[findLastFuncSymbolScope(curScope)]['Address'] + 4
            code = "(JP, @" + str(returnAddr) + ", , )"
            genCode[curAddrCode] = code
            curAddrCode += 1

    elif action == '#jr':
        returnAddr = symbTable[findLastFuncSymbol()]['Address'] + 4
        code = "(JP, @" + str(returnAddr) + ", , )"
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
        """if type(stack[-1]) != int and stack[-1][0] == '@':
            code = "(PRINT, " + str(stack[-1][1:]) + ", , )"
            genCode[curAddrCode] = code
            curAddrCode += 1
            code = "(PRINT, " + "604" + ", , )"
            genCode[curAddrCode] = code
            curAddrCode += 1"""
        if len(stack) > 1:
            lex = symbTable[getIdxByAddr(stack[-1])]["Lexeme"]
            #print(stack[-1])
            if type(stack[-1]) == int and stack[-1] < 1000:
                #print(lex, stack[-2], stack[-1], symbTable[findLex(lex, curScope)]["Address"])
                stack[-1] = symbTable[findLex(lex, curScope)]["Address"]
            #print(stack[-1])
            if symbTable[getIdxByAddr(stack[-1])]["Type"][-1] != "*" and symbTable[getIdxByAddr(stack[-1])]["FuncArrVar"] == 'Arr':
                code = '(ASSIGN, #' + str(stack[-1]) + ", " + str(stack[-2]) + ', )'
            #elif symbTable[getIdxByAddr(stack[-1])]["Type"][-1] == "*":
            #    code = '(ASSIGN, @' + str(stack[-1]) + ", " + str(stack[-2]) + ', )'
            else:
                code = '(ASSIGN, ' + str(stack[-1]) + ", " + str(stack[-2]) + ', )'
            stack.pop()
            stack.pop()
            genCode[curAddrCode] = code
            curAddrCode += 1

        """
        elif action == '#assign@':
        code = '(ASSIGN, ' + str(stack[-1]) + ", @" + str(stack[-2]) + ', )'
        stack.pop()
        stack.pop()
        genCode[curAddrCode] = code
        curAddrCode += 1
        """

    elif action == '#arrIdx':
        if len(stack) > 1:
            lex = symbTable[getIdxByAddr(stack[-2])]["Lexeme"]
            if findArrLex(lex, curScope) != -1:
                stack[-2] = symbTable[findArrLex(lex, curScope)]["Address"]
                #print(".............................................................",
                #      stack[-2], lex)
            temp = getTemp()
            code = '(MULT, ' + '#4' + ', ' + str(stack[-1]) + ', ' + str(temp) + ')'
            genCode[curAddrCode] = code
            curAddrCode += 1
            temp2 = getTemp()
            #print(stack)
            if symbTable[getIdxByAddr(stack[-2])]["Type"][-1] == "*":
                code = "(ADD, " + str(stack[-2]) + ", " + str(temp) + ", " + str(temp2) + ")"
            else:
                #print("boos.........................................................................", symbTable[getIdxByAddr(stack[-1])]["Lexeme"])
                code = "(ADD, #" + str(stack[-2]) + ", " + str(temp) + ", " + str(temp2) + ")"
            genCode[curAddrCode] = code
            stack.pop()
            stack.pop()
            stack.append('@' + str(temp2))
            curAddrCode += 1

    elif action == '#compare':
        if len(stack) > 2:
            temp = getTemp()
            if stack[-2] == '<':
                code = "(LT, " + str(stack[-3]) + ", " + str(stack[-1]) + ", " + str(temp) + ")"
            elif stack[-2] == '==':
                code = "(EQ, " + str(stack[-3]) + ", " + str(stack[-1]) + ", " + str(temp) + ")"
            genCode[curAddrCode] = code
            curAddrCode += 1
            stack.pop()
            stack.pop()
            stack.pop()
            stack.append(temp)
    elif action == '#mult':
        if len(stack) > 1:
            temp = getTemp()
            code = '(MULT, ' + str(stack[-1]) + ', ' + str(stack[-2]) + ', ' + str(temp) + ')'
            genCode[curAddrCode] = code
            curAddrCode += 1
            stack.pop()
            stack.pop()
            stack.append(temp)
    elif action == '#addMinus':
        if len(stack) > 2:
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
        if len(stack) > 0:
            if type(stack[-1]) != int and stack[-1][0] == '@':
                returnAddr = int(stack[-1][1:]) + 4
            else:
                returnAddr = int(stack[-1]) + 4
            code = '(ASSIGN, #' + str(curAddrCode + 2) + ", " + str(returnAddr) + ', )'
            genCode[curAddrCode] = code
            curAddrCode += 1

            codeAddr = symbTable[getIdxByAddr(stack[-1])]['CodeAddress']
            code = "(JP, " + str(codeAddr) + ", , )"
            genCode[curAddrCode] = code
            curAddrCode += 1

    elif action == '#pushReturn':
        if len(stack) > 0:
            if type(stack[-1]) != int and stack[-1][0] == '@':
                returnVal = int(stack[-1][1:]) + 8
            else:
                returnVal = int(stack[-1]) + 8

            if symbTable[getIdxByAddr(int(stack[-1]))]['Type'] == 'int':
                stack.pop()
                temp = getTemp()
                code = '(ASSIGN, ' + str(returnVal) + ", " + str(temp) + ', )'
                stack.append(temp)
                genCode[curAddrCode] = code
                curAddrCode += 1
            else:
                stack.pop()

    elif action == '#specDataAddrFunc':
        if len(stack) > 0:
            stack.append(stack[-1] + 12)

    elif action == '#pushAgain':
        if len(stack) > 0:
            stack.append(stack[-1])

    elif action == '#pushLen':
        stack.append(len(stack))
    elif action == '#popIf':
        if len(stack) > 1:
        #print("******:", len(stack), stack[-2] + 2)
            if len(stack) >= 2 and len(stack) == stack[-2] + 2:
                stack.pop()
                stack.pop()
            elif len(stack) == stack[-1] + 1:
                stack.pop()

    elif action == '#updateNextArgAddr':
        if len(stack) > 0:
            stack[-1] = stack[-1] + 4
            stack.append(stack[-1])

    elif action == '#popAgain':
        if len(stack) > 1:
            stack.pop()
            stack.pop()

    #elif action == '%args1':

    elif action == '%args2':
        lastSymbElem["No.Args"] = int(input)
        symbTable[-1] = lastSymbElem
    elif action == '%argsPush':
        argsStack.append(0)
    elif action == '%argsUpdateFunc':
        argsStack[-1] += 1
    elif action == '%zeroArgs':
        symbTable[findLastFuncSymbol()]["No.Args"] = argsStack[-1]
        argsStack.pop()

    elif action == '@popType':
        semanticStack.pop()

    elif action == '@pushTypeSpecifier':
        semanticStack.append(input)

    elif action == '@checkVoid':
        if semanticStack[-1] == 'void':
            if chk(lineCount - 3, lastSymbElem['Lexeme']):
                semantic_errors.append("#" + str(lineCount - 3) + " : Semantic Error! Illegal type of void for '" + lastSymbElem['Lexeme'] + "'.")
                semantic_errors_shdw.append(True)
                overall_errors.append((lineCount - 3, lastSymbElem['Lexeme']))
        semanticStack.pop()
    elif action == '@checkBreakInRepeatUntil':
        if len(breakPoints) <= 0:
            if chk(lineCount - 2, 'break'):
                semantic_errors.append("#" + str(lineCount - 2) + " : Semantic Error! No 'repeat ... until' found for 'break'.")
                semantic_errors_shdw.append(True)
                overall_errors.append((lineCount - 2, 'break'))

    elif action == '@pushType':
        if input.isnumeric():
            semanticStack.append('int')
        else:
            temp = symbTable[findLex(input, curScope)]["Type"]
            temp_2 = symbTable[findLex(input, curScope)]["FuncArrVar"]
            if findLex(input, curScope) == -1:
                semanticStack.append('error')
            elif temp == 'int' and temp_2 == 'Arr':
                semanticStack.append('array')
            elif temp == 'int*':
                semanticStack.append('array')
            else:
                semanticStack.append(temp)

    elif action == '@pushType3':
        if input.isnumeric():
            semanticStack.append('int')
        else:
            temp = symbTable[findLex(input, curScope)]["Type"]
            temp_2 = symbTable[findLex(input, curScope)]["FuncArrVar"]
            if temp == 'int' and temp_2 == 'Arr':
                semanticStack.append('array')
            elif temp == 'int*':
                semanticStack.append('array')
            else:
                semanticStack.append(temp)
    elif action == '@pushType2':
        semanticStack[-1] = 'int'

    elif action == '@initialCheckScope':
        if findLex(input, curScope) == -1:
            if chk(lineCount - 2, input):
                semantic_errors.append("#" + str(lineCount - 2) + " : Semantic Error! '" + input + "' is not defined.")
                semantic_errors_shdw.append(False)
                overall_errors.append((lineCount - 2, input))

    elif action == '@certain':
        if len(semantic_errors_shdw) > 0:
            semantic_errors_shdw[-1] = True
    elif action == '@checkScope':
        if input == '[':
            if findArrLex(symbTable[getIdxByAddr(stack[-1])]['Lexeme'], curScope) == -1:
                if len(semantic_errors_shdw) > 0 and not semantic_errors_shdw[-1]:
                    semantic_errors[-1] = "#" + str(lineCount - 2) + " : Semantic Error! '" + symbTable[getIdxByAddr(stack[-1])]['Lexeme'] + "' is not defined."
                    overall_errors[-1] = (lineCount - 2, symbTable[getIdxByAddr(stack[-1])]['Lexeme'])
                else:
                    if chk(lineCount - 2, symbTable[getIdxByAddr(stack[-1])]['Lexeme']):
                        semantic_errors.append("#" + str(lineCount - 2) + " : Semantic Error! '" + symbTable[getIdxByAddr(stack[-1])][
                            'Lexeme'] + "' is not defined.")
                        semantic_errors_shdw.append(True)
                        overall_errors.append((lineCount - 2, symbTable[getIdxByAddr(stack[-1])]['Lexeme']))
            else:
                if len(semantic_errors_shdw) != 0 and not semantic_errors_shdw[-1]:
                    semantic_errors.pop()
                    semantic_errors_shdw.pop()
                    overall_errors.pop()
        elif input == '(':
            if findFuncLex(symbTable[getIdxByAddr(stack[-1])]['Lexeme'], curScope) == -1:
                if not semantic_errors_shdw[-1]:
                    semantic_errors[-1] = "#" + str(lineCount - 2) + " : Semantic Error! '" + symbTable[getIdxByAddr(stack[-1])]['Lexeme'] + "' is not defined."
                    overall_errors[-1] = (lineCount - 2, symbTable[getIdxByAddr(stack[-1])]['Lexeme'])
                else:
                    if chk(lineCount - 2, symbTable[getIdxByAddr(stack[-1])]['Lexeme']):
                        semantic_errors.append("#" + str(lineCount - 2) + " : Semantic Error! '" + symbTable[getIdxByAddr(stack[-1])]['Lexeme'] + "' is not defined.")
                        semantic_errors_shdw.append(True)
                        overall_errors.append((lineCount - 2, symbTable[getIdxByAddr(stack[-1])]['Lexeme']))
            else:
                if len(semantic_errors_shdw) != 0 and not semantic_errors_shdw[-1]:
                    semantic_errors.pop()
                    semantic_errors_shdw.pop()
                    overall_errors.pop()
    elif action == '@checkSide':
        if semanticStack[-1] != 'error' and semanticStack[-2] != 'error' and semanticStack[-1] != semanticStack[-2]:
            if chk(lineCount - 2, "Type mismatch in operands"):
                semantic_errors.append("#" + str(lineCount - 2) + " : Semantic Error! Type mismatch in operands, Got " + semanticStack[-1] + " instead of " + semanticStack[-2] + ".")
                semantic_errors_shdw.append(True)
                overall_errors.append((lineCount - 2, "Type mismatch in operands"))
        temp = semanticStack[-2]
        semanticStack.pop()
        semanticStack.pop()
        semanticStack.append(temp)
    elif action == '@pushArgCount':
        funcArgsCountStack.append(0)
    elif action == '@incrementArgCount':
        print("x: ", funcArgsCountStack)
        funcArgsCountStack[-1] += 1
    elif action == '@checkArgs':
        if symbTable[getIdxByAddr(stack[-4])]["No.Args"] >= funcArgsCountStack[-1]:
            lex = symbTable[getIdxByAddr(stack[-1])]["Lexeme"]
            temp = symbTable[getIdxByAddr(stack[-1])]["Type"]
            temp_2 = symbTable[getIdxByAddr(stack[-1])]["FuncArrVar"]
            if type(stack[-1]) == int and stack[-1] < 1000:
                temp = symbTable[findLex(lex, curScope)]["Type"]
                temp_2 = symbTable[findLex(lex, curScope)]["FuncArrVar"]
            if temp == 'int*' or temp_2 == 'Arr':
                temp = 'array'
            temp_2 = symbTable[getIdxByAddr(stack[-2])]["Type"]
            if lineCount - 2 == 15:
                print(stack[-2], symbTable[getIdxByAddr(stack[-2])])
            if getIdxByAddr(stack[-2]) == -1:
                temp_2 = 'error'
            elif symbTable[getIdxByAddr(stack[-2])]["Type"] == 'int*' or symbTable[getIdxByAddr(stack[-2])]["FuncArrVar"] == 'Arr':
                temp_2 = 'array'
            if semanticStack[-1] != 'error' and temp_2 != 'error' and semanticStack[-1] != temp_2:
                if chk(lineCount - 2, str(funcArgsCountStack[-1])):
                    semantic_errors.append("#" + str(lineCount - 2) + " : Semantic Error! Mismatch in type of argument " + str(funcArgsCountStack[-1]) + " of '" + symbTable[getIdxByAddr(stack[-4])]["Lexeme"] + "'. Expected '" + temp_2 + "' but got '" + semanticStack[-1] + "' instead.")
                    semantic_errors_shdw.append(True)
                    overall_errors.append((lineCount - 2, str(funcArgsCountStack[-1])))
        semanticStack.pop()

    elif action == '@checkArgCountAndReset':
        #print(funcArgsCountStack)
        if symbTable[getIdxByAddr(stack[-1])]["No.Args"] != funcArgsCountStack[-1]:
            if chk(lineCount - 2, symbTable[getIdxByAddr(stack[-1])]["Lexeme"]):
                semantic_errors.append("#" + str(lineCount - 2) + " : Semantic Error! Mismatch in numbers of arguments of '" + symbTable[getIdxByAddr(stack[-1])]["Lexeme"] + "'.")
                semantic_errors_shdw.append(True)
                overall_errors.append((lineCount - 2, symbTable[getIdxByAddr(stack[-1])]["Lexeme"]))
            #for i in range(len(semantic_errors) - 1, -1, -1):
            #    if
        funcArgsCountStack.pop()

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
inputLine = 'void output (int a) {\n\t}\n' + inputLine
i = 0
flag_exit = 0
last_term_nonterm = ""
last_last_node = None
la_role, la_tok = get_next_token_parser()
last_la_tok = la_tok
parse_table_txt += 'Program\n'
while traverse_list and not flag_exit:
    match = False
    shdw = shadow.pop()
    nonTermshdw = nonTermShadow.pop()
    last_node = traverse_list.pop()
    #for u in range(len(traverse_list)):
    #    print(traverse_list[u].id, shadow[u], end=', ')
    #print(last_node.id)
    last_la_tok = la_tok
    if last_node.final:
        shadow.pop()
        last_last_node = traverse_list.pop()
        last_term_nonterm = nonTermShadow.pop()
        #print(last_node.from_ops)
        for t in last_node.from_ops:
            #print("............................")
            #print(t[0].id, last_last_node.id)
            #print(t[1], last_term_nonterm)
            #print("............................")
            if last_term_nonterm == t[1] and last_last_node.id == t[0].id:
                for x in last_node.from_ops[t]:
                    codeGen(x, la_tok)
        while len(shadow) > 0 and shadow[-1]:
            shadow.pop()
            nonTermShadow.pop()
            last_node = last_last_node
            last_last_node = traverse_list.pop()
            if last_node.final:
                #print(last_last_node, last_node.from_ops)
                for t in last_node.from_ops:
                    if last_term_nonterm == t[1] and last_last_node == t[0]:
                        for x in last_node.from_ops[t]:
                            codeGen(x, la_tok)
        continue

    if shdw == True:
        continue

    for term_nonterm, node in last_node.to.items():
        #print(la_tok)
        last_term_nonterm = term_nonterm
        last_last_node = last_node
        res = getNonTermByName(term_nonterm)
        edge_type = last_edge if node.final else middle_edge
        if res:
            if la_role == 'NUM' or la_role == 'ID':
                if la_role in res.first:
                    shadow.append(True)
                    nonTermShadow.append(term_nonterm)
                    traverse_list.append(last_node)
                    write_nonterm(node, res, edge_type)
                    match = True
                    break
                elif 'EPSILON' in res.first and la_role in res.follow:
                    shadow.append(True)
                    nonTermShadow.append(term_nonterm)
                    traverse_list.append(last_node)
                    write_nonterm(node, res, edge_type)
                    match = True
                    break
            else:
                if la_tok in res.first:
                    shadow.append(True)
                    nonTermShadow.append(term_nonterm)
                    traverse_list.append(last_node)
                    write_nonterm(node, res, edge_type)
                    match = True
                    break
                elif 'EPSILON' in res.first and la_tok in res.follow:
                    shadow.append(True)
                    nonTermShadow.append(term_nonterm)
                    traverse_list.append(last_node)
                    write_nonterm(node, res, edge_type)
                    match = True
                    break
        else:
            if la_role == 'NUM' or la_role == 'ID':
                if la_role == term_nonterm:
                    shadow.append(True)
                    nonTermShadow.append(term_nonterm)
                    traverse_list.append(last_node)
                    write_term(node, la_role, la_tok, edge_type)
                    last_la_tok = la_tok
                    la_role, la_tok = get_next_token_parser()
                    match = True
                    break
                elif term_nonterm == 'EPSILON' and la_role in node.final.follow:
                    shadow.append(True)
                    nonTermShadow.append(term_nonterm)
                    traverse_list.append(last_node)
                    write_epsilon(node, edge_type, )
                    match = True
                    break
            else:
                if la_tok == term_nonterm:
                    shadow.append(True)
                    nonTermShadow.append(term_nonterm)
                    traverse_list.append(last_node)
                    write_term(node, la_role, la_tok, edge_type)
                    last_la_tok = la_tok
                    la_role, la_tok = get_next_token_parser()
                    match = True
                    break
                elif term_nonterm == 'EPSILON' and la_tok in node.final.follow:
                    shadow.append(True)
                    nonTermShadow.append(term_nonterm)
                    traverse_list.append(last_node)
                    write_epsilon(node, edge_type)
                    match = True
                    break
    if match:
        #print(last_node.id)
        if term_nonterm in last_node.to_ops:
            for x in last_node.to_ops[term_nonterm]:
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
                        shadow.append(False)
                        nonTermShadow.append("")
                        traverse_list.append(node)
                        flag = True
                        err_name = term_nonterm
                        break
                else:
                    if la_tok in res.follow:
                        syntax_error_txt += f'#{lineCount} : syntax error, missing {term_nonterm}\n'
                        shadow.append(False)
                        nonTermShadow.append("")
                        traverse_list.append(node)
                        flag = True
                        break
            else:
                if len(last_node.to) == 1:
                    syntax_error_txt += f'#{lineCount} : syntax error, missing {term_nonterm}\n'
                    shadow.append(False)
                    nonTermShadow.append("")
                    traverse_list.append(node)
                    flag = True
                    break
        if not flag and not flag_exit:
            syntax_error_txt += f'#{lineCount} : syntax error, illegal {la_role if la_role == "ID" or la_role == "NUM" else la_tok}\n'
            shadow.append(False)
            nonTermShadow.append("")
            traverse_list.append(last_node)
            last_la_tok = la_tok
            la_role, la_tok = get_next_token_parser()
            flag = False

write_file_lexical()
write_file_parser()
write_generated_code()
write_symb_table()
write_semantic_errors()
