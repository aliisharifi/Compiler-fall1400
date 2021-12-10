import re
# Ali Sharifi 98109601
# Hamid Reza Dehbashi 98105762

def get_next_token_compiler():
    global table, lineCount, state, tokens, errors, symbolTable, keywords, openComment, startComment, i
    x, lineCount, state, tokens, errors, symbolTable, keywords, openComment, startComment, i = get_next_token_scanner(inputLine, table, lineCount, state, tokens, errors, symbolTable, keywords, openComment, startComment, i)
    return x


class Node:
    idLen = 0
    nodes = []

    def __init__(self):
        self.id = Node.idLen
        Node.idLen += 1
        Node.nodes.append(self)
        # pointer to nonterminal (if one exists :))
        self.start = None
        self.final = None
        self.to = {}


class NonTerminal:
    idLen = 0
    nonTerminals = []

    def __init__(self, name):
        self.name = name
        self.id = NonTerminal.idLen
        NonTerminal.idLen += 1
        NonTerminal.nonTerminals.append(self)
        # pointer to node
        self.start = None
        self.final = None
        self.first = []
        self.follow = []
        self.predict = []


def getNonTermByName(name, nonTerminals):
    for nonterm in nonTerminals:
        if nonterm.name == name:
            return nonterm
    return None


def get_next_token_parser():
    role, token = get_next_token_compiler()
    return (role, token)
    """returns (role, token)"""
    pass


def initialize_first(nonTerminals):
    with open('first.txt', 'r') as file:
        frstTxt = file.readlines()

    terminals = frstTxt[0].split('\t')
    for i in range(len(terminals)):
        if terminals[i] == 'Îµ\n':
            terminals[i] = 'EPSILON'
    # for i in range(0, len(frstTxt[0])):
    print(terminals)
    for i in range(1, len(frstTxt)):
        tempStr = frstTxt[i].split("\t")
        nontermName = tempStr[0]
        nonterm = getNonTermByName(nontermName, nonTerminals)
        if i == 2:
            print(tempStr)
        for j in range(1, len(tempStr)):
            if tempStr[j] == '+' or tempStr[j] == '+\n':
                nonterm.first.append(terminals[j - 1])
    return nonTerminals


def initialize_follow(nonTerminals):
    with open('follow.txt', 'r') as file:
        fllwTxt = file.readlines()

    terminals = fllwTxt[0].split('\t')
    for i in range(len(terminals)):
        if terminals[i] == 'â”¤\n':
            terminals[i] = '@'
    # for i in range(0, len(frstTxt[0])):
    for i in range(1, len(fllwTxt)):
        tempStr = fllwTxt[i].split("\t")
        nontermName = tempStr[0]
        nonterm = getNonTermByName(nontermName, nonTerminals)
        for j in range(1, len(tempStr)):
            if tempStr[j] == '+' or tempStr[j] == '+\n':
                nonterm.follow.append(terminals[j - 1])
    return nonTerminals


def initialize_nodes():
    grmstr = ""
    with open('newGr2.txt', 'r') as file:
        grmstr = file.readlines()

    nodes = []
    nonTerminals = []
    nameToId = {}
    for i in range(0, len(grmstr)):
        x = re.search("(\\d+)\. (.+)", grmstr[i])
        grmstr[i] = x.group(2)
        x = re.search("(.+) -> (.+)", grmstr[i])
        nonterm = NonTerminal(x.group(1))
        nameToId.update({x.group(1): nonterm.id})
        nonTerminals.append(nonterm)
    for i in range(0, len(grmstr)):
        x = re.search("(.+) -> (.+)", grmstr[i])
        nonterm = getNonTermByName(x.group(1), nonTerminals)
        startNode = Node()
        nodes.append(startNode)
        finalNode = Node()
        nodes.append(finalNode)
        startNode.start = nonterm
        finalNode.final = nonterm
        nonterm.start = startNode
        nonterm.final = finalNode
        rules_str = x.group(2)
        rules = rules_str.split('|')
        for Rule in rules:
            lastNode = startNode
            rule = Rule.split(" ")
            q = 0
            while q < len(rule):
                if rule[q] == '':
                    rule.pop(q)
                    q -= 1
                q += 1
            if len(rule) == 1:
                startNode.to.update({rule[0]: finalNode})
            # print(rule)
            for j in range(0, len(rule) - 1):
                temp = Node()
                nodes.append(temp)
                # print(temp.id)
                lastNode.to.update({rule[j]: temp})
                lastNode = temp
            lastNode.to.update({rule[len(rule) - 1]: finalNode})
    return nodes, nonTerminals


def initialize_parser():
    nodes, nonTerminals = initialize_nodes()
    nonTerminals = initialize_first(nonTerminals)
    nonTerminals = initialize_follow(nonTerminals)
    parse_table_txt = ""
    syntax_error_txt = ""
    traverse_list = [nodes[0]]
    middle_edge = '├── '
    last_edge = '└── '
    cont_edges = '│   '
    space = '    '
    return nodes, nonTerminals, parse_table_txt, syntax_error_txt, traverse_list, middle_edge, last_edge, cont_edges, space


"""
def write_file():
    f = open('parse_table.txt', mode='w+')
    e = open('syntax_errors.txt', mode='w+')
"""


def write_file(parse_table_txt, syntax_errors_txt):
    with open('parse_table.txt', mode='w') as f:
        f.write(parse_table_txt)
    with open('syntax_errors.txt', mode='w') as e:
        e.write(syntax_errors_txt)


"""
def write_nonterm(node_, res_, edge_type_):
    # f.write(calc_line_first_part() + branch_edges + res_.name + '\n')

    f.write(calc_line_first_part() + edge_type_ + res_.name + '\n')
    traverse_list.append(node_)
    traverse_list.append(res_)
"""


def write_nonterm(node_, res_, edge_type_, parse_table_txt, traverse_list, cont_edges, space):
    # f.write(calc_line_first_part() + branch_edges + res_.name + '\n')

    # f.write(calc_line_first_part() + edge_type_ + res_.name + '\n')
    parse_table_txt += calc_line_first_part(traverse_list, cont_edges, space) + edge_type_ + res_.name + '\n'
    traverse_list.append(node_)
    traverse_list.append(res_)
    return parse_table_txt, traverse_list


"""
def write_term(node_, la_role_, la_tok_, edge_type_):
    # f.write(calc_line_first_part() + branch_edges + '(' + la_role_ + ', ' + la_tok_ + ')' + '\n')
    f.write(calc_line_first_part() + edge_type_ + '(' + la_role_ + ', ' + la_tok_ + ')' + '\n')
    traverse_list.append(node_)
"""


def write_term(node_, la_role_, la_tok_, edge_type_, parse_table_txt, traverse_list, cont_edges, space):
    # f.write(calc_line_first_part() + branch_edges + '(' + la_role_ + ', ' + la_tok_ + ')' + '\n')
    # f.write(calc_line_first_part() + edge_type_ + '(' + la_role_ + ', ' + la_tok_ + ')' + '\n')
    parse_table_txt += calc_line_first_part(traverse_list, cont_edges,
                                            space) + edge_type_ + '(' + la_role_ + ', ' + la_tok_ + ')' + '\n'
    traverse_list.append(node_)
    return parse_table_txt, traverse_list


"""
def write_epsilon(node_, edge_type_):
    # f.write(calc_line_first_part() + branch_edges + 'EPSILON' + '\n')
    f.write(calc_line_first_part() + edge_type_ + 'EPSILON' + '\n')
    traverse_list.append(node_)
"""


def write_epsilon(node_, edge_type_, parse_table_txt, traverse_list, cont_edges, space):
    # f.write(calc_line_first_part() + branch_edges + 'EPSILON' + '\n')
    # f.write(calc_line_first_part() + edge_type_ + 'EPSILON' + '\n')
    parse_table_txt += calc_line_first_part(traverse_list, cont_edges, space) + edge_type_ + 'EPSILON' + '\n'
    traverse_list.append(node_)
    return parse_table_txt, traverse_list


def calc_line_first_part(traverse_list, cont_edges, space):
    line_first_part = ''
    for node in traverse_list:
        if node.final:
            line_first_part += space
        else:
            line_first_part += cont_edges
    # pass
    return line_first_part


def run_parser(nodes, nonTerminals, parse_table_txt, syntax_error_txt, traverse_list, middle_edge, last_edge,
               cont_edges, space, lineCount):
    la_role, la_tok = get_next_token_parser()
    # f.write('Program\n')
    parse_table_txt += 'Program\n'
    while traverse_list:
        match = False
        last_node = traverse_list.pop()
        if last_node.final:
            while True:
                if la_role == 'NUM' or la_role == 'ID':
                    if la_role in last_node.final.follow:
                        break
                    else:
                        # illegal
                        syntax_error_txt += f'#{lineCount} : syntax error, illegal {la_role}\n'
                        la_role, la_tok = get_next_token_parser()
                else:
                    if la_tok in last_node.final.follow:
                        break
                    else:
                        # illegal
                        syntax_error_txt += f'#{lineCount} : syntax error, illegal {la_tok}\n'
                        la_role, la_tok = get_next_token_parser()
            continue
        for term_nonterm, node in last_node.to.items():
            res = getNonTermByName(term_nonterm, nonTerminals)
            edge_type = last_edge if node.final else middle_edge
            if res:
                if la_role == 'NUM' or la_role == 'ID':
                    if la_role in res.first:
                        parse_table_txt, traverse_list = write_nonterm(node, res, edge_type, parse_table_txt,
                                                                       traverse_list, cont_edges, space)
                        match = True
                        break
                    elif 'EPSILON' in res.first and la_role in res.follow:
                        parse_table_txt, traverse_list = write_nonterm(node, res, edge_type, parse_table_txt,
                                                                       traverse_list, cont_edges, space)
                        match = True
                        break
                else:
                    if la_tok in res.first:
                        parse_table_txt, traverse_list = write_nonterm(node, res, edge_type, parse_table_txt,
                                                                       traverse_list, cont_edges, space)
                        match = True
                        break
                    elif 'EPSILON' in res.first and la_tok in res.follow:
                        parse_table_txt, traverse_list = write_nonterm(node, res, edge_type, parse_table_txt,
                                                                       traverse_list, cont_edges, space)
                        match = True
                        break
            else:
                if la_role == 'NUM' or la_role == 'ID':
                    if la_role == term_nonterm:
                        parse_table_txt, traverse_list = write_term(node, la_role, la_tok, edge_type, parse_table_txt,
                                                                    traverse_list, cont_edges, space)
                        match = True
                        break
                    elif term_nonterm == 'EPSILON' and la_role in node.final.follow:
                        parse_table_txt, traverse_list = write_epsilon(node, edge_type, parse_table_txt, traverse_list,
                                                                       cont_edges, space)
                        match = True
                        break
                else:
                    if la_tok == term_nonterm:
                        parse_table_txt, traverse_list = write_term(node, la_role, la_tok, edge_type, parse_table_txt,
                                                                    traverse_list, cont_edges, space)
                        match = True
                        break
                    elif term_nonterm == 'EPSILON' and la_tok in node.final.follow:
                        parse_table_txt, traverse_list = write_epsilon(node, edge_type, parse_table_txt, traverse_list,
                                                                       cont_edges, space)

                        match = True
                        break
        if match:
            la_role, la_tok = get_next_token_parser()
            match = False
        else:
            # asumption : last_node has only one edge
            # term_nonterm, node = list(last_node.to).pop()
            flag, err_name = False, None
            for term_nonterm, node in last_node.to.items():
                res = getNonTermByName(term_nonterm, nonTerminals)
                if res:
                    if la_role == 'NUM' or la_role == 'ID':
                        if la_role in res.follow:
                            # pring missing
                            syntax_error_txt += f'#{lineCount} : syntax error, missing {term_nonterm}\n'
                            traverse_list.append(node)
                            flag = True
                            err_name = term_nonterm
                            break
                        # else:
                        #     # print illegal
                        #     traverse_list.append(last_node)
                        #     la_role, la_tok = get_next_token()
                    else:
                        if la_tok in res.follow:
                            # print missing
                            syntax_error_txt += f'#{lineCount} : syntax error, missing {term_nonterm}\n'
                            traverse_list.append(node)
                            flag = True
                            err_name = term_nonterm
                            break
                        # else:
                        #     # print illegal
                        #     traverse_list.append(last_node)
                        #     la_role, la_tok = get_next_token()
                else:
                    if len(last_node.to) == 1:
                        # print missing
                        syntax_error_txt += f'#{lineCount} : syntax error, missing {term_nonterm}\n'
                        traverse_list.append(node)
                        flag = True
                        err_name = term_nonterm
                        break
            if not flag:
                # print illegal
                syntax_error_txt += f'#{lineCount} : syntax error, illegal {err_name}\n'
                traverse_list.append(last_node)
                la_role, la_tok = get_next_token_parser()
                flag = False

    return parse_table_txt, syntax_error_txt, traverse_list


def addToken(token, lexeme_temp, line, tokens):
    """
    Gets a token and puts its lexeme on the corresponding line in the tokens table
    """
    if line not in tokens:
        tokens.update({line: []})
    tokens[line].append((token, lexeme_temp))
    return tokens

def addError(lexeme_temp, error, line, errors):
    """
    Gets an error and puts its lexeme on the corresponding line in the error table
    """
    if line not in errors:
        errors.update({line: []})
    errors[line].append((lexeme_temp, error))
    return errors

def addSymbolTable(lexeme_temp, symbolTable):
    """
    Gets an id and puts it on the corresponding line in the symbol table
    """
    if lexeme_temp not in symbolTable:
        symbolTable.update({lexeme_temp: len(symbolTable) + 1})
    return symbolTable

def initSymbolTable(keywords, symbolTable):
    """
    Puts keywords on the beginning of the symbol table
    """
    for xX in keywords:
        symbolTable.update({xX: len(symbolTable) + 1})
    return symbolTable

def initScanner():

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

    # Auxiliary variables
    lineCount = 1
    state = ""
    tokens = {}
    errors = {}
    symbolTable = {}
    keywords = ["if", "else", "void", "int", "repeat", "break", "until", "return", "endif"]
    openComment = False
    startComment = -1
    symbolTable = initSymbolTable(keywords, symbolTable)
    returnList = [table, lineCount, state, tokens, errors, symbolTable, keywords, openComment, startComment]
    return returnList

#f = open('input.txt', 'r')
#inputLine = f.read()


def get_next_token_scanner(inputLine, table, lineCount, state, tokens, errors, symbolTable, keywords, openComment, startComment, i):
    ret = ''
    if i == len(inputLine):
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
                    tokens = addToken("KEYWORD", lexeme, lineCount, tokens)
                    ret = ('KEYWORD', lexeme)
                else:
                    tokens = addToken("ID", lexeme, lineCount, tokens)
                    ret = ('ID', lexeme)
                    symbolTable = addSymbolTable(lexeme, symbolTable)
                i -= 1

            elif state == "ID_KEY_ACC":
                if lexeme in keywords:
                    tokens = addToken("KEYWORD", lexeme, lineCount, tokens)
                    ret = ('KEYWORD', lexeme)
                else:
                    tokens = addToken("ID", lexeme, lineCount, tokens)
                    ret = ('ID', lexeme)
                    symbolTable = addSymbolTable(lexeme, symbolTable)

            elif state == "invalid_input":
                errors = addError(lexeme, "Invalid input", lineCount, errors)

            elif state == "invalid_input_*":
                if inputLine[i] == '\n':
                    lineCount -= 1
                errors = addError(lexeme[0: len(lexeme) - 1], "Invalid input", lineCount, errors)
                i -= 1

            elif state == "invalid_number":
                errors = addError(lexeme, "Invalid number", lineCount, errors)

            elif state == "NUM_ACC_*":
                if inputLine[i] == '\n':
                    lineCount -= 1
                tokens = addToken("NUM", lexeme[0: len(lexeme) - 1], lineCount, tokens)
                ret = ('NUM', lexeme[0:len(lexeme) - 1])
                i -= 1

            elif state == "NUM_ACC":
                tokens = addToken("NUM", lexeme, lineCount, tokens)
                ret = ('NUM', lexeme)

            elif state == "unmatched_comment":
                errors = addError(lexeme, "Unmatched comment", lineCount, errors)

            elif state == "COM_1_ACC":
                openComment = False

            elif state == "COM_2_ACC":
                openComment = False

            elif state == "unclosed_comment":
                openComment = False
                if len(lexeme) > 7:
                    lexeme = lexeme[0:7] + "..."
                errors = addError(lexeme, "Unclosed comment", startComment, errors)

            elif state == "symbol_1":
                tokens = addToken("SYMBOL", lexeme, lineCount, tokens)
                ret = ('SYMBOL', lexeme)

            elif state == "symbol_3":
                tokens = addToken("SYMBOL", lexeme, lineCount, tokens)
                ret = ('SYMBOL', lexeme)

            elif state == "symbol_4_*":
                if inputLine[i] == '\n':
                    lineCount -= 1
                tokens = addToken("SYMBOL", lexeme[0: len(lexeme) - 1], lineCount, tokens)
                ret = ('SYMBOL', lexeme[0:len(lexeme) - 1])
                i -= 1

            elif state == "symbol_4":
                tokens = addToken("SYMBOL", lexeme, lineCount, tokens)
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
        return ret, lineCount, state, tokens, errors, symbolTable, keywords, openComment, startComment, i

def write_tokens(tokens):  # Reformat tokens in tokenTxt
    tokenTxt = ""
    for i in tokens:
        tokenTxt += str(i).strip('"\'') + ".	"
        for x in tokens[i]:
            tokenTxt += "(" + str(x[0]).strip('"\'') + ", " + str(x[1]).strip('"\'') + ")" + " "
        tokenTxt += "\n"
    return tokenTxt

def write_symbolTable(symbolTable):# Reformat symbol table in symbolTxt
    symbolTxt = ""
    for i in symbolTable:
        symbolTxt += str(symbolTable[i]).strip('"\'') + ".	" + str(i).strip('"\'')
        symbolTxt += "\n"
    return symbolTxt

def wirte_lexical_errors(errors): # Reformat errors in errorTxt
    errorTxt = ""
    for i in errors:
        errorTxt += str(i).strip('"\'') + ".	"
        for x in errors[i]:
            errorTxt += "(" + str(x[0]).strip('"\'') + ", " + str(x[1]).strip('"\'') + ")" + " "
        errorTxt += "\n"
    if len(errors) == 0:
        errorTxt = "There is no lexical error."

def write_file(errorTxt, tokenTxt, symbolTxt):
    # Write in file
    with open("lexical_errors.txt", "w") as lexical:
        lexical.write(errorTxt)

    with open("tokens.txt", "w") as tokenFile:
        tokenFile.write(tokenTxt)

    with open("symbol_table.txt", "w") as symbolFile:
        symbolFile.write(symbolTxt)




i = 0
with open('input.txt', 'r') as f:
    inputLine = f.read()

nodes, nonTerminals, parse_table_txt, syntax_error_txt, traverse_list, middle_edge, last_edge, cont_edges, space \
    = initialize_parser()

table, lineCount, state, tokens, errors, symbolTable, keywords, openComment, startComment = initScanner()

run_parser(nodes, nonTerminals, parse_table_txt, syntax_error_txt, traverse_list, middle_edge, last_edge, cont_edges, space, lineCount)

write_file(wirte_lexical_errors(errors), write_tokens(tokens), write_symbolTable(symbolTable))
write_file(parse_table_txt, syntax_error_txt)


# e.close()
# f.close()

# lecture example
# input : (id)
# 0
# 1 7
# 1 8 14
# 1 8 15
# 1 8 16 0
# 1 8 16 1 7
# 1 8 16 1 8 14
# 1 8 16 1 8 17
# 1 8 16 1 9 10
# 1 8 16 1 9 13
# 1 8 16 1 9
# 1 8 16 1
# 1 8 16 2 3
# 1 8 16 2 6
# 1 8 16 2
# 1 8 16
# 1 8 17
# 1 8
# 1 9 10
# 1 9 13
# 1 9
# 1
# 2 3
# 2 6
# 2
# :)


# E
# |___T
# |   |___F
# |       |___(
#         |___E
#             |

