import scanner
import parser

i = 0
with open('input.txt', 'r') as f:
    inputLine = f.read()

table, lineCount, state, tokens, errors, symbolTable, keywords, openComment, startComment = scanner.initScanner()

nodes, nonTerminals = parser.initialize_first_follow_nodes()


def get_next_token():
    global table, lineCount, state, tokens, errors, symbolTable, keywords, openComment, startComment, i
    x, lineCount, state, tokens, errors, symbolTable, keywords, openComment, startComment, i = scanner.get_next_token(inputLine, table, lineCount, state, tokens, errors, symbolTable, keywords, openComment, startComment, i)
    return x


