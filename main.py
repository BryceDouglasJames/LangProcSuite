# Charlie DeGennaro
import sys
in_file = sys.argv[1]


class Dfa:
    def __init__(self, start_state, accept_states, table):
        self.start_state = start_state
        self.accept_states = accept_states
        self.table = table

    def __str__(self):
        return 'Start State: ' + self.start_state + '\nAccept States: ' + str(self.accept_states) + '\nTable: ' + str(self.table)

    def init_from_file(in_file, trace=False):
        with open(in_file, "r") as f:
            file = f.readlines()
        f.close()
        dfa_table = {}
        lines_index = 0
        # First remove all newlines and blank lines
        while lines_index < len(file):
            file[lines_index] = file[lines_index].replace('\n', '')
            # If line is empty, remove it
            if file[lines_index] == '':
                file.remove('')
            # If line is not empty, then we can move to next index
            else:
                lines_index += 1
        if trace:
            print(1, file)

        # Second, remove all comments on empty lines
        lines_index = 0
        while lines_index < len(file):
            if file[lines_index].replace(' ', '')[:2] == '//':
                file.remove(file[lines_index])
            else:
                lines_index += 1
        if trace:
            print(2, file)

        # Third, get start state and accept states, and remove them from file
        start_state = file[0]
        accept_states = file[1].replace(' ', '').split(',')
        file = file[2:]
        if trace:
            print(3, file, start_state, accept_states)

        # Fourth, convert file to list of lists seperated by spaces
        lines_index = 0
        while lines_index < len(file):
            file[lines_index] = file[lines_index].split(' ')
            if '' in file[lines_index]:
                file[lines_index].remove('')
            lines_index += 1
        if trace:
            print(4, file)

        # Fifth, construct the dfa_table using the parsed information in file
        for line in file:
            if len(line) != 3:
                print('Error on state with following structure:', line)
                return {}
            if line[0] not in dfa_table:
                dfa_table[line[0]] = {}
            dfa_table[line[0]][line[1]] = line[2]
        if trace:
            print(5, dfa_table)

        return Dfa(start_state, accept_states, dfa_table)

    def check_string(self, input, trace=False):
        cur_state = self.start_state
        for char in input:
            if trace:
                print('[', cur_state, ' ', char, '] -> ', sep='', end='')
            cur_state = self.table[cur_state][char]
        if trace:
            print('[', cur_state, ']', sep='')

        return cur_state in self.accept_states


dfa = Dfa.init_from_file(in_file)

print(dfa)

print(dfa.check_string('aabbabaabbbbbaab', True))
