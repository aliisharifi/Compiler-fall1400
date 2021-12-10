import scanner
import parser

table, lineCount, state, tokens, errors, symbolTable, keywords, openComment, startComment = scanner.initScanner()

nodes, nonTerminals = parser.initialize_first_follow_nodes()

