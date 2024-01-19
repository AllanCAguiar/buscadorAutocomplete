from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=["http://localhost:9200"])

if es.ping():
    print(f"Conectado ao cluster Elasticsearch: {es.info().get('cluster_name')}")
else:
    print("Falha na conexão com o Elasticsearch")

index_name = 'buscas'

# Leitura do conteúdo do arquivo e inserção no Elasticsearch
with open("dataset/jusbrasil.txt", "r") as arquivo:
    linhas = arquivo.readlines()

    for i, linha in enumerate(linhas, start=1):
        document = {
            "id": i,
            "texto": linha.strip()
        }

        # Indexe o documento no Elasticsearch
        es.index(index=index_name, body=document)

print(f"Total de {len(linhas)} documentos inseridos no índice '{index_name}'")
