import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        add_help=True, description='Sample Commandline')

    parser.add_argument(
        '--grammar',
        action="store",
        help="path of file to take as input to read grammar",
        nargs="?",
        metavar="dfa_file")
    parser.add_argument(
        '--input',
        action="store",
        help="path of file to take as input to test strings on LL table",
        nargs="?",
        metavar="input_file")

    args = parser.parse_args()

    print(args.grammar)
    print(args.input)

    inputDFAFile = args.grammar
    fileTestCases = args.input

    file_outLL1 = open("task_6_1_result.txt", "a")
    file_outInput = open("task_6_2_result.txt", "a")

    terminals = set()
    Nonterminal = set()

    LL_1_ = {}

    dictRules = {}

    inputString = "a a"
    valid = True
    i = 1
    startVariable = "start"

    with open(inputDFAFile, 'r') as f:
        lines = f.readlines()
        print("Grammar", lines)

    with open(fileTestCases, 'r') as f:
        linesString = f.readlines()
        inputString = linesString[0]
        print("linesString", linesString)

    for line in lines:
        line = line.strip()
        symbRuleFirstFollow = line.split(":")
        if i == 1:
            startVariable = symbRuleFirstFollow[0].strip()
            i += 1
        dictRules[symbRuleFirstFollow[0].strip()] = {
            'rules': symbRuleFirstFollow[1].split("|"),
            'first': symbRuleFirstFollow[2].split(" "),
            'follow': symbRuleFirstFollow[3].split(" ")
        }
        dictRules[symbRuleFirstFollow[0].strip()]['first'] = [
            value
            for value in dictRules[symbRuleFirstFollow[0].strip()]['first']
            if value != ''
        ]

        dictRules[symbRuleFirstFollow[0].strip()]['follow'] = [
            value
            for value in dictRules[symbRuleFirstFollow[0].strip()]['follow']
            if value != ''
        ]
        terminals = terminals.union(
            dictRules[symbRuleFirstFollow[0].strip()]['first'])
        terminals = terminals.union(
            dictRules[symbRuleFirstFollow[0].strip()]['follow'])

        Nonterminal.add(symbRuleFirstFollow[0].strip())
        print(symbRuleFirstFollow)

    if 'epsilon' in terminals:
        terminals.remove('epsilon')

    print("dictRules", dictRules)
    print("Nonterminal", Nonterminal)

    def constLL1():
        global LL_1_
        global valid

        for symbol in Nonterminal:
            rules = dictRules[symbol]["rules"]
            LL_1_[symbol] = {}
            terminalsSoFar = []
            for term in terminals:
                LL_1_[symbol][term] = {}

            for rule in rules:
                ruleArry = rule.split(" ")
                ruleArry = [value for value in ruleArry if value != '']
                i = 0
                notBreak = True
                if ruleArry[i] in Nonterminal:
                    while notBreak:
                        if ruleArry[i] not in Nonterminal:
                            if ruleArry[i] not in terminalsSoFar:
                                LL_1_[symbol][ruleArry[i]] = rule
                                terminalsSoFar.append(ruleArry[i])
                            else:
                                file_outLL1.write("invalid LL(1) grammar")
                                print('invalid LL(1) grammar')
                                valid = False
                                return

                            break

                        terminalofsymbolFirst = dictRules[ruleArry[i]]['first']

                        for terminal in terminalofsymbolFirst:
                            if terminal != 'epsilon':
                                if terminal not in terminalsSoFar:
                                    LL_1_[symbol][terminal] = rule
                                    terminalsSoFar.append(terminal)
                                else:
                                    file_outLL1.write("invalid LL(1) grammar")
                                    print('invalid LL(1) grammar')
                                    valid = False
                                    return

                        notBreak = False
                        if 'epsilon' in dictRules[ruleArry[i]]['rules']:
                            notBreak = True
                            i += 1
                else:
                    if ruleArry[i] != 'epsilon':
                        if ruleArry[i] not in terminalsSoFar:
                            LL_1_[symbol][ruleArry[i]] = rule
                            terminalsSoFar.append(ruleArry[i])
                        else:
                            file_outLL1.write("invalid LL(1) grammar")
                            print('invalid LL(1) grammar')
                            valid = False
                            return

                    else:
                        for followrule in dictRules[symbol]['follow']:
                            if followrule not in terminalsSoFar:
                                LL_1_[symbol][followrule] = ruleArry[i]
                                terminalsSoFar.append(followrule)
                            else:
                                file_outLL1.write("invalid LL(1) grammar")
                                print('invalid LL(1) grammar')
                                valid = False
                                return

    def parseInput():
        inputStringArry = inputString.split(" ")
        print(inputStringArry)
        inputStringArry.append('$')
        print(startVariable)
        stackArr = ['$', startVariable]
        print(stackArr)
        indexInput = 0

        while indexInput < len(inputStringArry):
            peekarray = stackArr[len(stackArr) - 1]
            charCurrent = inputStringArry[indexInput]
            if peekarray in Nonterminal:
                if LL_1_[peekarray][charCurrent]:
                    rule = LL_1_[peekarray][charCurrent]
                    ruleArry = rule.split(" ")
                    ruleArry = [value for value in ruleArry if value != '']
                    ruleArry = list(reversed(ruleArry))
                    stackArr.pop()
                    stackArr.extend(ruleArry)
                else:
                    return False

            else:
                if peekarray == '$' and charCurrent != '$':
                    return False
                if peekarray == 'epsilon':
                    stackArr.pop()
                else:
                    if peekarray == charCurrent:
                        stackArr.pop()
                        indexInput += 1
                    elif peekarray != charCurrent:
                        return False

        if len(stackArr) > 0:
            return False

        return True

    constLL1()

    def printOutLL():

        for key in LL_1_:
            stringLine = "" + key + " : "
            for item, value in LL_1_[key].items():

                if value:
                    if value == "epsilon":
                        stringitem = "" + item + " : " + value
                    else:
                        stringitem = "" + item + " :" + value

                else:

                    value = " "
                    stringitem = "" + item + " :" + value

                strAll = stringLine + stringitem
                file_outLL1.write(strAll)
                file_outLL1.write("\n")

    if valid:
        printOutLL()
        if parseInput():
            file_outInput.write("yes")
            print("yes")
        else:
            file_outInput.write("no")
            print("no")
    else:
        file_outInput.write("no")
        print("no")

    print("LL_1_", LL_1_)
