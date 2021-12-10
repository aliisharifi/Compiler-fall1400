def get_next_token():
    """returns (role, token)"""
    pass

f = open('parse_table.txt', mode='w+')
e = open('syntax_errors.txt', mode='w+')


la_role, la_tok = get_next_token()
# node with id 0?
traverse_list = []
f.write('Program\n')
branch_edges = '|--- '
cont_edges = '|    '
space = '    '

def write_nonterm(node_, res_):
    f.write(calc_line_first_part() + branch_edges + res_.name + '\n')
    traverse_list.append(node_)
    traverse_list.append(res_)

def write_term(node_, la_role_, la_tok_):
    f.write(calc_line_first_part() + branch_edges + '(' + la_role_ + ', ' + la_tok_ + ')' + '\n')
    traverse_list.append(node_)

def write_epsilon(node_):
    f.write(calc_line_first_part() + branch_edges + 'EPSILON' + '\n')
    traverse_list.append(node_)

# def get_node_nonterm:
#     """returns the nonterminal of the diagram that node belongs to"""
#     pass

def calc_line_first_part():
    line_first_part = ''
    for node in traverse_list:
        if node.final:
            line_first_part += space
        else:
            line_first_part += cont_edges
    pass

# while look_ahead != '$':
while traverse_list:
    match = False
    last_node = traverse_list.pop()
    if last_node.final:
        while True:
            if la_role == 'NUM' or la_role == 'ID':
                if la_role in last_node.final.follow:
                    break
                # if la_role not in last_node.final.follow:
                else:
                    # illegal
                    la_role, la_tok = get_next_token()
            else:
                if la_tok in last_node.final.follow:
                    break
                # if la_tok not in last_node.final.follow:
                else:
                    # illegal
                    la_role, la_tok = get_next_token()
        continue
    for term_nonterm, node in last_node.to.items():
        res = getNonTermByName(term_nonterm)
        if res:
            if la_role == 'NUM' or la_role == 'ID':
                if la_role in res.first:
                    write_nonterm(node, res)
                    match = True
                    break
                elif 'EPSILON' in res.first and la_role in res.follow:
                    write_nonterm(node, res)
                    match = True
                    break
            else:
                if la_tok in res.first:
                    write_nonterm(node, res)
                    match = True
                    break
                elif 'EPSILON' in res.first and la_tok in res.follow:
                    write_nonterm(node, res)
                    match = True
                    break 
        else:
            if la_role == 'NUM' or la_role == 'ID':
                if la_role == term_nonterm:
                    write_term(node, la_role, la_tok)
                    match = True
                    break
                elif term_nonterm == 'EPSILON' and la_role in node.final.follow:
                    write_epsilon(node)
                    match = True
                    break
            else:
                if la_tok == term_nonterm:
                    write_term(node, la_role, la_tok)
                    match = True
                    break
                elif term_nonterm == 'EPSILON' and la_tok in node.final.follow:
                    write_epsilon(node)
                    match = True
                    break
    # la_role, la_tok = get_next_token()
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

e.close()
f.close()




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
