# Bryce James :)
import sys

Non_Terms = {}
Terms = {}
Term_Strings = {}


def __init__():
    print("RUNNIN PREDICT/FOLLOW/FIRST SETS")


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
        print(source)

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
            if not N_Term in Non_Terms:
                Non_Terms[N_Term] = []
                Non_Terms[N_Term].append(P_String)
            else:
                Non_Terms[N_Term].append(P_String)

            print(N_Term + " :::: " + P_String)
            start_line += 1

        print(str(Non_Terms))
        pass
    else:
        raise RuntimeError(
            "Please enter proper file format for source .grm...")
