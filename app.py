from flask import Flask, jsonify, request
from flask_cors import CORS

from cyk_parser.cyk_tree import CYKParser
from cyk_parser.grammar import Grammar
from cyk_parser.parse_tree import Tree

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)

# set grammar file
grammar_file = 'cyk_parser/grammars/english.txt'

def get_tree(sentence):
    parser = CYKParser(grammar_file)
    table = parser.generate_cyk_table(sentence)
    root = parser.build_tree(table, 'S', row=len(table)-1, col=0)
    if root is None:
        error = {"error": "Ungrammatical sentence"}
        return jsonify(error)
    tree = Tree(root)
    data = tree.serialize()
    return jsonify(data)

@app.route('/', methods=['GET', 'POST'])
def parse():
    sentence = 'fish swim in streams'
    if request.method == 'POST':
        sentence = str(request.get_json()['value'].lower())
    return get_tree(sentence)

@app.route('/grammar/', methods=['GET'])
def grammar():
    grammar = Grammar(grammar_file)
    data = grammar.serialize()
    return jsonify(data)


if __name__ == '__main__':
    app.run()
