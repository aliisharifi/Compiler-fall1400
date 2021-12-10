import re

import compiler
import scanner

i = 0
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


def getNonTermByName(name):
    for nonterm in NonTerminal.nonTerminals:
        if nonterm.name == name:
            return nonterm
    return None


def get_next_token():
    role, token = compiler.get_next_token()
    return (role, token)
    """returns (role, token)"""
    pass


def initialize_first():
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
        nonterm = getNonTermByName(nontermName)
        if i == 2:
            print(tempStr)
        for j in range(1, len(tempStr)):
            if tempStr[j] == '+' or tempStr[j] == '+\n':
                nonterm.first.append(terminals[j - 1])


def initialize_follow():
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
        nonterm = getNonTermByName(nontermName)
        for j in range(1, len(tempStr)):
            if tempStr[j] == '+' or tempStr[j] == '+\n':
                nonterm.follow.append(terminals[j - 1])


def initialize_nodes():
    grmstr = ""
    with open('newGr2.txt', 'r') as file:
        grmstr = file.readlines()

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
        nonterm = getNonTermByName(x.group(1))
        startNode = Node()
        finalNode = Node()
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
                # print(temp.id)
                lastNode.to.update({rule[j]: temp})
                lastNode = temp
            lastNode.to.update({rule[len(rule) - 1]: finalNode})


def initialize_parser():
    initialize_nodes()
    initialize_first()
    initialize_follow()
    parse_table_txt = ""
    syntax_error_txt = ""
    traverse_list = []
    middle_edge = '├── '
    last_edge = '└── '
    cont_edges = '│   '
    space = '    '
    return Node.nodes, NonTerminal.nonTerminals, parse_table_txt, syntax_error_txt, traverse_list, middle_edge, last_edge, cont_edges, space
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

    #f.write(calc_line_first_part() + edge_type_ + res_.name + '\n')
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
    #f.write(calc_line_first_part() + edge_type_ + '(' + la_role_ + ', ' + la_tok_ + ')' + '\n')
    parse_table_txt += calc_line_first_part(traverse_list, cont_edges, space) + edge_type_ + '(' + la_role_ + ', ' + la_tok_ + ')' + '\n'
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
    #f.write(calc_line_first_part() + edge_type_ + 'EPSILON' + '\n')
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
    #pass
    return line_first_part

def run_parser(nodes, nonTerminals, parse_table_txt, syntax_error_txt, traverse_list, middle_edge, last_edge, cont_edges, space, lineCount):
    la_role, la_tok = get_next_token()
    # node with id 0?

    #f.write('Program\n')
    parse_table_txt += 'Program\n'
    # while look_ahead != '$':
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
                        la_role, la_tok = get_next_token()
                else:
                    if la_tok in last_node.final.follow:
                        break
                    else:
                        # illegal
                        la_role, la_tok = get_next_token()
            continue
        for term_nonterm, node in last_node.to.items():
            res = getNonTermByName(term_nonterm)
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
            la_role, la_tok = get_next_token()
            match = False
        else:
            # asumption : last_node has only one edge
            term_nonterm, node = list(last_node.to).pop()
            res = getNonTermByName(term_nonterm)
            if res:
                if la_role == 'NUM' or la_role == 'ID':
                    if la_role in res.follow:
                        # pring missing
                        traverse_list.append(node)
                    else:
                        # print illegal
                        traverse_list.append(last_node)
                        la_role, la_tok = get_next_token()
                else:
                    if la_tok in res.follow:
                        # print missing
                        traverse_list.append(node)
                    else:
                        # print illegal
                        traverse_list.append(last_node)
                        la_role, la_tok = get_next_token()
            else:
                # print missing
                traverse_list.append(node)
    return parse_table_txt, syntax_error_txt, traverse_list

#e.close()
#f.close()

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
