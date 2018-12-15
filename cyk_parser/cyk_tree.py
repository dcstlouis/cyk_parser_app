import itertools
from .parse_tree import Node, Tree

class Cell:

    def __init__(self, symbol=None, symbol_set=None, left=None, right=None):
        self._symbol = symbol
        self._symbol_set = symbol_set
        self._left = left
        self._right = right

    def __str__(self):
        cell = f"Cell: "
        symbol = f"Symbol = {self._symbol}, "
        set = f"Set = {self._symbol_set}, "
        children = f"Children = {self._left}, {self._right}"
        return cell + symbol + set + children

    @property
    def symbol_set(self):
        return self._symbol_set

    @symbol_set.setter
    def symbol_set(self, value):
        self._symbol_set = value

    @property
    def children(self):
        return (self._left, self._right)

    @children.setter
    def children(self, left, right):
        self._left = left
        self._right = right

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, cell):
        self._left = cell

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, cell):
        self._right = cell

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, symbol):
        self._symbol = symbol


class CYKParser:

    def __init__(self, grammar_file):
        self.grammar = self.import_grammar(grammar_file)
        self.reverse_grammar = self.generate_reverse_grammar()

    def import_grammar(self, grammar_file):
        # grammar = OrderedDict()
        grammar = {}
        with open(grammar_file, 'r', encoding='utf-8') as f:
            for production in f:
                p = production.replace('\n', "").split('->')
                variable = p[0].strip()
                symbols = p[1].strip()
                try:
                    grammar[variable].append(symbols)
                except KeyError:
                    grammar[variable] = [symbols]
        return grammar

    def generate_reverse_grammar(self):
        """Creates a grammar to look up variables from terminals"""
        # reverse_grammar = OrderedDict()
        reverse_grammar = {}
        for key in self.grammar.keys():
            symbols = self.grammar[key]
            for symbol in symbols:
                try:
                    reverse_grammar[symbol].add(key)
                except KeyError:
                    reverse_grammar[symbol] = set([key]) # avoid duplicates
        return reverse_grammar

    def lookup_symbol(self, symbol):
        """
        if symbol can be produced by a set of terminals or variables
        in the grammar, then return that set. else return an empty set
        """
        try:
            s = self.reverse_grammar[symbol]
            return s
        except KeyError:
            return set()

    def is_in_grammar(self, s):
        """Uses the CYK algorithm to determine whether s is a valid string"""
        print(s)
        sentence = s
        # sentence = s.split()
        n = len(sentence)

        # Start by filling table with empty sets
        table = [[set() for w in sentence] for w in sentence]

        # Fill bottom of table
        for i, w in enumerate(sentence):
            table[0][i] = self.lookup_symbol(w)

        # Now use CYK algorithm to fill in the rest of the table
        for row in range(1, n):
            for col in range(n - row):
                for t in range(row):
                    try:
                        a = table[t][col]
                        b = table[row-t-1][col+t+1]
                        pairs = itertools.product(a,b) # cartesian product
                        for p in pairs:
                            symbol = "".join(p)
                            symbol_set = self.lookup_symbol(symbol)
                            union = table[row][col].union(symbol_set)
                            table[row][col] = union
                    except IndexError as e:
                        print(e)
                        pass
        return(table[n-1][0])


    def generate_cyk_table(self, s):
        sentence = s
        sentence = s.split()
        n = len(sentence)

        # Start by filling table with empty lists
        table = [[[] for w in sentence] for w in sentence]

        # Fill bottom of table
        for i, w in enumerate(sentence):
            table[0][i].append(Cell(symbol=w, symbol_set=self.lookup_symbol(w)))

        # Now use CYK algorithm to fill in the rest of the table
        for row in range(1, n):
            for col in range(n - row):
                for t in range(row):
                    try:
                        a_set, b_set = set(), set()
                        for cell in table[t][col]:
                            a_set = a_set.union(cell.symbol_set)
                        for cell in table[row-t-1][col+t+1]:
                            b_set = b_set.union(cell.symbol_set)
                        pairs = itertools.product(a_set, b_set)
                        for p in pairs:
                            symbol = "".join(p)
                            symbol_set = self.lookup_symbol(symbol)
                            left = (t, col)
                            right = (row-t-1, col+t+1)
                            new_cell = Cell(symbol=symbol,
                                            symbol_set=symbol_set,
                                            left=left, right=right)
                            table[row][col].append(new_cell)
                    except IndexError as e:
                        print(e)
                        pass

        return table

    def build_tree(self, table, label, row=None, col=None):
        if row == None and col == None:
            return
        root = None
        for cell in table[row][col]:
            if label in cell.symbol_set:
                symbol = cell.symbol

                # left child
                if symbol.isupper():
                    # symbol is a variable
                    left_label = symbol[0]
                else:
                    # symbol is a terminal
                    left_label = symbol
                if cell.left != None:
                    left = self.build_tree(table, left_label, cell.left[0], cell.left[1])
                else:
                    left = Node(label=left_label)

                # right child
                if symbol.isupper():
                    # symbol is a variable
                    right_label = symbol[1]
                    if cell.right != None:
                        right = self.build_tree(table, right_label, cell.right[0], cell.right[1])
                    else:
                        right = Node(label=right_label)
                else:
                    # symbol is a terminal
                    # (and shouldn't have a right child)
                    right = None

                root = Node(label=label, left=left, right=right)

        return root
