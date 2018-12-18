from flask import Flask, jsonify, request
from flask_cors import CORS

from cyk_parser.cyk_tree import CYKParser
from cyk_parser.parse_tree import Tree

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)

def get_tree(sentence):
    parser = CYKParser('cyk_parser/grammars/english.txt')
    table = parser.generate_cyk_table(sentence)
    root = parser.build_tree(table, 'S', row=len(table)-1, col=0)
    if root is None:
        print(f"Ungrammatical sentence: {sentence}")
    tree = Tree(root)
    data = tree.serialize()
    return jsonify(data)

@app.route('/', methods=['GET', 'POST'])
def parse():
    sentence = 'fish swim in streams'
    if request.method == 'POST':
        sentence = str(request.get_json()['value'].lower())
    return get_tree(sentence)


if __name__ == '__main__':
    app.run()
