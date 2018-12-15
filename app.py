from flask import Flask, jsonify
from flask_cors import CORS

from cyk_parser.cyk_tree import CYKParser
from cyk_parser.parse_tree import Tree

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)

@app.route('/', methods=['GET'])
@app.route('/parse', methods=['GET'])
def parse():
    parser = CYKParser('cyk_parser/grammars/english.txt')
    table = parser.generate_cyk_table("amy ate fish for dinner on tuesday")
    root = parser.build_tree(table, 'S', row=len(table)-1, col=0)
    tree = Tree(root)
    return jsonify(tree.serialize())


if __name__ == '__main__':
    app.run()
