# Charlie DeGennaro
import sys
in_file = sys.argv[1]
in_file2 = sys.argv[2]


class Dfa:
    def __init__(self, start_state, accept_states, table, state_list, char_list):
        self.start_state = start_state
        self.accept_states = accept_states
        self.table = table
        self.state_list = state_list
        self.char_list = char_list

    def __str__(self):
        return 'Start State: ' + self.start_state + '\nAccept States: ' + str(self.accept_states) + '\nTable: ' + str(self.table)

    def init_from_list(file, trace=False):
        dfa_table = []
        state_list = {}
        char_list = {}
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

        # Second, remove all comments
        lines_index = 0
        while lines_index < len(file):
            if file[lines_index].replace(' ', '')[:2] == '//':
                file.remove(file[lines_index])
            else:
                file[lines_index] = file[lines_index].split('//')[0]
                lines_index += 1
        if trace:
            print(2, file)

        # Third, get start state and accept states, and remove them from file
        start_state = file[0]
        accept_states = file[1].replace(' ', '').split(',')
        file = file[2:]
        if trace:
            print(3, file, start_state, accept_states)

        # Fourth, convert file to list of lists seperated by spaces, also build character list
        lines_index = 0
        while lines_index < len(file):
            file[lines_index] = file[lines_index].split(' ')
            if '' in file[lines_index]:
                file[lines_index].remove('')
            if file[lines_index][1] not in char_list:
                char_list[file[lines_index][1]] = len(char_list)
            lines_index += 1
        if trace:
            print(4, file, char_list)

        # Fifth, construct the dfa_table using the parsed information in file
        for line in file:
            if len(line) != 3:
                print('Error on state with following structure:', line)
                return Dfa('', '', '')
            if line[0] not in state_list.keys():
                state_list[line[0]] = len(dfa_table)
                dfa_table.append([None]*(len(char_list)))
            dfa_table[state_list[line[0]]][char_list[line[1]]] = line[2]
        if trace:
            print(5, dfa_table, state_list)

        return Dfa(start_state, accept_states, dfa_table, state_list, char_list)

    def check_string(self, input, trace=False):
        cur_state = self.start_state
        for char in input:
            if trace:
                print('[', cur_state, ' ', char, '] -> ', sep='', end='')
            cur_state = self.table[self.state_list[cur_state]
                                   ][self.char_list[char]]
        if trace:
            print('[', cur_state, ']', sep='')

        return cur_state in self.accept_states

    def init_from_file(in_file, trace=False):
        with open(in_file, "r") as f:
            file = f.readlines()
        f.close()
        return Dfa.init_from_list(file, trace)


class Nfa:
    def __init__(self, start_state, accept_states, table, char_list, state_list):
        self.start_state = start_state
        self.accept_states = accept_states
        self.table = table
        self.char_list = char_list
        self.state_list = state_list

    def __str__(self):
        return 'Start State: ' + self.start_state + '\nAccept States: ' + str(self.accept_states) + '\nTable: ' + str(self.table)

    def init_from_file(in_file, trace=False):
        with open(in_file, "r") as f:
            file = f.readlines()
        f.close()
        nfa_table = []
        state_list = {}
        char_list = {}
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

        # Second, remove all comments
        lines_index = 0
        while lines_index < len(file):
            if file[lines_index].replace(' ', '')[:2] == '//':
                file.remove(file[lines_index])
            else:
                file[lines_index] = file[lines_index].split('//')[0]
                lines_index += 1
        if trace:
            print(2, file)

        # Third, get start state and accept states, and remove them from file
        start_state = file[0]
        accept_states = file[1].replace(' ', '').split(',')
        file = file[2:]
        if trace:
            print(3, file, start_state, accept_states)

        # Fourth, convert file to list of lists seperated by spaces, also build character list
        lines_index = 0
        while lines_index < len(file):
            file[lines_index] = file[lines_index].split(' ')
            if '' in file[lines_index]:
                file[lines_index].remove('')
            if file[lines_index][1] not in char_list:
                if file[lines_index][1] != '^':
                    char_list[file[lines_index][1]] = len(char_list)
            lines_index += 1
        char_list['^'] = len(char_list)
        if trace:
            print(4, file, char_list)

        # Fifth, construct the nfa_table using the parsed information in file
        for line in file:
            if len(line) != 3:
                print('Error on state with following structure:', line)
                return None
            if line[0] not in state_list.keys():
                state_list[line[0]] = len(nfa_table)
                nfa_table.append([[] for _ in range(len(char_list))])
                nfa_table[state_list[line[0]]
                          ][len(char_list)-1].append(line[0])
            if line[2] not in nfa_table[state_list[line[0]]][char_list[line[1]]]:
                nfa_table[state_list[line[0]]
                          ][char_list[line[1]]].append(line[2])
        if trace:
            print(5, nfa_table, char_list, state_list)

        # Sixth, sort the internal lists
        for row in nfa_table:
            for column in row:
                column.sort()
        if trace:
            print(6, nfa_table)

        return Nfa(start_state, accept_states, nfa_table, char_list, state_list)

    def nfa_to_dfa(self):
        cur_set = ''
        table_incrementer = 0
        conversion_table = []  # DFA_Index Set char1 char2...

        conversion_table.append([1, self.start_state])
        conversion_index = [self.start_state]

        # print(self.table)

        while table_incrementer < len(conversion_table):
            for char in self.char_list:
                # print(char)
                cur_set = ''
                converstion_states = conversion_table[table_incrementer][1].split(
                    ',')
                states = []
                # print('cs', converstion_states)
                for state in converstion_states:
                    if state in self.table.keys():
                        if char in self.table[state].keys():
                            states.append(self.table[state][char])
                if len(states) == 0:
                    states = ['']
                # print('st', states)
                for locations in states:
                    for state in locations:
                        if state not in cur_set:
                            cur_set += state + ','
                cur_set = cur_set[:-1]
                if cur_set not in conversion_index:
                    conversion_index.append(cur_set)
                    conversion_table.append([len(conversion_index), cur_set])
                conversion_table[table_incrementer].append(
                    conversion_index.index(cur_set)+1)
            # print(conversion_table)
            table_incrementer += 1

        # print(conversion_table)

        # Convert conversion_table to dfa list format
        dfa_list = []
        dfa_list.append(self.start_state)
        accept_states = ''
        for state in conversion_index:
            states = state.split(',')
            for sub_state in states:
                if sub_state in self.accept_states and state not in accept_states:
                    accept_states += str(conversion_index.index(state)+1) + ','
        dfa_list.append(accept_states[:-1])
        for conv in conversion_table:
            mod_conv = conv[2:]
            for i in range(len(mod_conv)):
                dfa_list.append(str(conv[0]) + ' ' +
                                self.char_list[i] + ' ' + str(mod_conv[i]))

        # print(dfa_list)
        return Dfa.init_from_list(dfa_list)

    def check_string(self, input, trace=False):
        cur_state = self.start_state
        for char in input:
            if trace:
                print('[', cur_state, ' ', char, '] -> ', sep='', end='')
            cur_state = self.table[cur_state][char]
        if trace:
            print('[', cur_state, ']', sep='')

        return cur_state in self.accept_states


# dfa = Dfa.init_from_file(in_file, True)

# print(dfa)

# print(dfa.check_string('aabbaab', True))

nfa = Nfa.init_from_file(in_file2, True)

print(nfa)

# dfa2 = nfa.nfa_to_dfa()
# print(dfa2)

# print(dfa2.check_string('aabbaab', True))
