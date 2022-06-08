# Bryce James :)
import sys
sys.setrecursionlimit(100)

Productions = {}
Terms = []
Term_Strings = {}
split_at = 0

if len(sys.argv) == 1:
    # CLI Custom Input
    outputFilename = sys.argv[0] + '.grm'

    # TODO List client steps and index productions
    raise RuntimeError("Have not implemented custom input just yet.... :(")
elif sys.argv[1] == '-h' or sys.argv[1] == '--help':
    # help flag
    exit("Usage:\n\t python3 PFFSets.py <Filename>.grm: Read from grammar file\n\t python3 PFFSets.py: Custom input\n")
elif len(sys.argv) == 2:
    if sys.argv[1].split('.')[-1] == 'grm':

        # Get file and strip empty lines
        outputFilename = sys.argv[1].split('.')[-1] + '.grm'
        infile = open(sys.argv[1], 'r')
        source = infile.read().splitlines()
        source = [i for i in source if i]
        # print(source)

        # Compile regexes (Options)
        import re
        p_string_val = re.compile(
            r"[!,%,@, $,^,*,?,_,~,.,>,<,\/,{,},\[,\],|,\\]+$")
        comment = re.compile(r'//')

        # pass 1 check for weird stuff and comments
        start_line = 0
        for line in source:

            # Check for comment line... should just check all with single regex but oh well
            if not comment.search(line) == None:
                is_comment = len(comment.search(line).group())
            else:
                is_comment = 0

            # verify starting line
            if is_comment > 0:
                source[start_line] = ""
                start_line += 1
                continue

            start_line += 1

        # Fix source code
        source = [i for i in source if i]

        # pass 2 index all nontermials with production strings
        start_line = 0
        for line in source:
            Product_List = line.strip(" ").split('->')
            N_Term = Product_List[0].strip()
            P_String = Product_List[1].strip()
            if not N_Term.isupper() or len(N_Term[0]) > 1:
                raise RuntimeError(
                    "Please start production " + str(start_line + 1) + " with a single capital letter. This will change later but for now... srry")

            if p_string_val.search(P_String) != None:
                print(P_String)
                raise RuntimeError(
                    "Error parsing production " + source[start_line] + " : invalid production string.")

            # TODO Map each nonTerminal with the production string.
            if not N_Term in Productions:
                Productions[N_Term] = []
                Productions[N_Term].append(P_String)
            else:
                Productions[N_Term].append(P_String)

            for c in P_String:
                if c.islower():
                    if c not in Terms:
                        Terms.append(c)

            print(N_Term + " :::: " + P_String)
            start_line += 1

        def first(term):
            temp = []
            # if a non-terminal is being handled
            if term in Productions.keys():
                prod = Productions[term]
                #print("THIS IS THE PROD %s for term %s" % (prod, term))
                for terms in prod:
                    # recursively find first and set it
                    temp2 = first(terms)
                    temp = list(set(temp) | set(temp2))

            # if string is a terminal
            elif term.islower():
                temp = {term}

            # if string equals nothing, EOF, or lambda
            elif term == '':
                temp = {''}

            else:
                # if we can't find anything, this means the statement starts with a non-terminal.
                # Handling lambdas is annoying but hey
                temp2 = first(term[0])
                if '' in temp2:
                    i = 1
                    while '' in temp2:
                        temp = list(set(temp) | (set(temp2) - {''}))
                        if term[i:].islower():
                            temp = list(set(temp) | set(term[i:]))
                            break
                        elif term[i:] == '':
                            temp = list(set(temp) | {''})
                            break
                        temp2 = first(term[i:])
                        temp = list(set(temp) | (set(temp2) - {''}))
                        i += 1
                else:
                    temp = list(set(temp) | set(temp2))
            return list(temp)

        # make first dictionary and set keys as non terminals
        FIRST = {}
        for i in Productions:
            for p in i:
                FIRST[p] = []

        # iterate grammar and pass each production to recursive function
        for nt, s_arr in Productions.items():
            for s in s_arr:
                FIRST[nt] = first(nt)

        # verify the grammar is in fact LL(1) before continuing
        vals = set()
        count = 0
        for nt, s_arr in Productions.items():
            for s in s_arr:
                vals.add(s)
                count += 1
        if count != len(vals):
            raise RuntimeError(
                "This grammar does not appear LL(1). Please fix the grammar before continuing.")
        print("FIRST SET: ", FIRST)

        ###########################

        # def find_right(nt, s):
        #    c = s[0]
        #    print(s)
        #    if c.islower():
        #        FOLLOW[nt].append(c)
        #    elif s == "":
        #        pass
        #        # IF THE FIRST ENCOUNTER IS LAMBDA, JUST UNION FOLLOW SETS
        #        # f_set = FOLLOW[nt]
        #        # if len(f_set) != 0:
        #        #    temp = list(set(FOLLOW[c]) | set(f_set))
        #        #    FOLLOW[c] = temp
        #    elif c.isupper() and s != "":
        #        # GET FIRST SET FOR THIS NON TERM AND ADD TO FOLLOW
        #        f_set = FOLLOW[nt]
        #        # if len(f_set) != 0:
        #        temp = list(set(FIRST[c]) | set(f_set))
        #        print("OH BOYYYYYYYY ", temp)
        #        FOLLOW[c] = temp
        #    else:
        #        raise RuntimeError(
        #            "Something went wrong when pasrsing rigth side for follow...")
        #    return

        # def parseFollow(c, s):
        #    global split_at
        #    left = s[:split_at]
        #    right = s[split_at:]

        #    # TODO this the hard part
        #    # if right is not empty, create follow set and add left part to be handled. Otherwise just add left part.
        #    if c == '' or s == '' or len(s) == 1:
        #        return
        #    elif right != "":
        #        # pass
        #        # FOLLOW[nt].append(right)
        #        # FOLLOW_QUEUE[nt].append(left)
        #        # parseFollow(left[-1], left)
        #        find_right(c, right)
        #    else:
        #        # pass
        #        # FOLLOW_QUEUE[nt].append(left)
        #        # parseFollow(left[-1], left)
        #        f_set = FOLLOW[nt]
        #        # if len(f_set) != 0:
        #        temp = list(set(FOLLOW[c]) | set(f_set))
        #        print("OH BOYYYYYYYY ", temp)
        #        FOLLOW[c] = temp

        #    print(str(left) + "::::" + str(right))

        # MAKE FOLLOW SET
        #FOLLOW = {}
        #FOLLOW_QUEUE = {}
        # for i in Productions:
        #    for p in i:
        #        FOLLOW[p] = []
        #        FOLLOW_QUEUE[p] = []
        #print("FOLLOW ", FOLLOW)

        # for nt, s_arr in Productions.items():
        #    for s in s_arr:
        #        split_at = 1
        #        for c in s:
        #            # USE RECURSIVE FUNCTION TO PARSE PRODUCTION
        #            if c.isupper():
        #                parseFollow(c, s)
        #            if s == "":
        #                break

        # for nt, s_arr in FOLLOW_QUEUE.items():
        #    for s in s_arr:
        #        temp_non_term = s[1][-1].strip()
        #        f_set = FOLLOW[nt]
        #        if len(f_set) != 0:
        #            temp = list(set(FOLLOW[temp_non_term]) | set(f_set))
        #            FOLLOW[temp_non_term] = temp
        #        print("THIS FOLLOW  " + temp_non_term +
        #              " : ", FOLLOW[temp_non_term])

    #print("FOLLOW QUEUE: ", FOLLOW_QUEUE)
    #print("FOLLOW: ", FOLLOW)
    # print(FIRST)
    # print(str(Productions))
    else:
        raise RuntimeError(
            "Please enter proper file format for source .grm...")
