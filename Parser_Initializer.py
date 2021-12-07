import re

class Node:
    idLen = 0

    def __init__(self):
        self.id = Node.idLen
        Node.idLen += 1
        self.start = None
        self.final = None
        self.to = {}


class NonTerminal:
    idLen = 0

    def __init__(self, name):
        self.name = name
        self.id = NonTerminal.idLen
        NonTerminal.idLen += 1
        self.start = None
        self.final = None


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


def getNonTermByName(name):
    for nonterm in nonTerminals:
        if nonterm.name == name:
            return nonterm
    return None

def dfs(node):
    tempX = node
    for i in range(0, len(node.to)):
        temp = node
        print(temp.id, "\tby\t", list(temp.to.keys())[i], "\t->\t", end="")
        tempX = dfs(list(temp.to.values())[i])
    return tempX

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
        #print(rule)
        for j in range(0, len(rule) - 1):
            temp = Node()
            #print(temp.id)
            lastNode.to.update({rule[j]: temp})
            lastNode = temp
        lastNode.to.update({rule[len(rule) - 1]: finalNode})
        #print(list(lastNode.to.values())[0].id)
#marked = []
#for i in range(Node.idLen):
#   marked.append(0)
for nonterm in nonTerminals:
    print(nonterm.name, ": ")
    for i in range(0, len(nonterm.start.to)):
        temp = nonterm.start
        tempX = nonterm.start
#        print("X: ", list(nonterm.start.to)[i], marked[list(temp.to.values())[i].id])
        print(temp.id, "\tby\t", list(temp.to)[i], "\t->\t", end="")
        temp = list(temp.to.values())[i]
        tempX = dfs(temp)

        if len(list(tempX.to.values())) == 0:
            print(tempX.id)
        else:
            print(list(tempX.to.values())[0].id)

"""
x = ""
with open('grammers.txt', 'r') as file:
    x = file.read()
x = x.replace('-', '_')
x = x.replace("_>", "->")
with open('newGr2.txt', 'w') as file:
    file.write(x)

"""