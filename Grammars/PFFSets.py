# Bryce James :)
import sys

def __init__():
    print("RUNNIN PREDICT/FOLLOW/FIRST SETS")


if sys.argv[1] == '-h' or sys.argv[1] == '--help':
    # help flag
    exit("Usage:\n\t python3 PFFSets.py <Filename>.grm: Read from grammar file\n\t python3 PFFSets.py: Custom input\n")
elif len(sys.argv) == 1:
    # CLI Custom Input
    outputFilename = sys.argv[0] + '.grm'

    # TODO List client steps and index productions
    pass

elif len(sys.argv) == 2:
    if sys.argv[1].split('.')[-1] == 'grm':
        outputFilename = sys.argv[1].split('.')[0] + '.fa'
        infile = open(sys.argv[1], 'r')
        source = infile.read().splitlines()

        # TODO Parse each production. Map each nonTerminal with the production string.
        pass
    else:
        raise RuntimeError(
            "Please enter proper file format for source .grm...")
