from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=["http://localhost:9200"])

if es.ping():
    print(f"Conectado ao cluster Elasticsearch: {es.info().get('cluster_name')}")
else:
    print("Falha na conexão com o Elasticsearch")

index_name = 'buscas_suggester'

settings = {
    "mappings": {
        "properties": {
            "texto": {
                "type": "text",
                "fields": {
                    "suggest": {
                        "type": "completion"
                    }
                }
            },
            "peso": {
                "type": "integer"
            }
        }
    }
}


print(es.indices.create(index=index_name, body=settings, ignore=400))

