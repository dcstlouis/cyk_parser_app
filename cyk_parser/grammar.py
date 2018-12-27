import csv

class Grammar:

    def __init__(self, grammar_file):
        self.grammar = self.import_grammar(grammar_file)

    def import_grammar(self, grammar_file):
        grammar = []
        with open(grammar_file, 'r', encoding='utf-8') as f:
            for production in f:
                p = production.replace('\n', "").split('->')
                variable = p[0].strip()
                symbols = p[1].strip()
                grammar.append((variable, symbols))
        return grammar

    def serialize(self):
        serialization = {'grammar': self.grammar}
        return serialization
