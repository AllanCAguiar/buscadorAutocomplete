from elasticsearch import Elasticsearch

# Conecte-se ao Elasticsearch (certifique-se de ter o Elasticsearch em execução)
es = Elasticsearch(hosts=["http://127.0.0.1:9200"])

# Verifique se a conexão foi bem-sucedida
if es.ping():
    print(f"Conectado ao cluster Elasticsearch: {es.info().get('cluster_name')}")
else:
    print("Falha na conexão com o Elasticsearch")

# Nome do índice no qual você deseja inserir documentos
index_name = 'buscas'

# Leitura do conteúdo do arquivo e inserção no Elasticsearch
with open("jusbrasil.txt", "r") as arquivo:
    linhas = arquivo.readlines()

    for i, linha in enumerate(linhas, start=1):
        document = {
            "id": i,
            "texto": linha.strip()
        }

        # Indexe o documento no Elasticsearch
        es.index(index=index_name, body=document)

print(f"Total de {len(linhas)} documentos inseridos no índice '{index_name}'")
