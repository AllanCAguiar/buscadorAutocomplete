from flask import Flask, request, jsonify, render_template
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme':'http'}])

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')

    if not query:
        return jsonify({'error': 'Query parameter "q" is required'}), 400

    body = {
            'suggest': {
                'sugestao': {
                    "prefix": query,
                    "completion": {
                        "field": "texto.suggest",
                        "size": 10,
                        "fuzzy": {
                            "fuzziness": 1
                        }
                    }
                }
            }
        }

    result = es.search(index='buscas', body=body)  
    hits = [option['_source'] for option in result['suggest']['sugestao'][0]['options']]    
    results = [hit['texto'] for hit in hits]
    print(result['took'])
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
