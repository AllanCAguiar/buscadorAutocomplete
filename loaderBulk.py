from elasticsearch import Elasticsearch
from elasticsearch.helpers import parallel_bulk
import concurrent.futures

def extrair_docs_do_arquivo(caminho_do_arquivo):
    docs = []
    
    with open(caminho_do_arquivo, 'r', encoding='utf-8') as arquivo:        
        for linha in arquivo:
            if linha:
                docs.append(linha.strip())
    return docs

def combinar_linhas(doc1, doc2):
    # Combina uma linha do doc1 com uma linha do doc2
    return "{}\t{}".format(doc1, doc2)

def construirDocumento(doc1, doc2):
    return {      
        "suggest" : {
            "input": [doc1],
            "weight" : int(float(doc2))
        }
    }

def indexar_documento(documento):
    # Lógica para indexar ou atualizar o documento no Elasticsearch
    # Substitua isso com sua própria lógica de indexação
    return {
        "_op_type": "index",
        "_index": "buscas_suggester",
        "_source": {"conteudo": documento}
    }

caminho_do_arquivo1 = 'dataset/jusbrasil-topk.txt'
caminho_do_arquivo2 = 'dataset/scores.txt'

documentos1 = extrair_docs_do_arquivo(caminho_do_arquivo1)
documentos2 = extrair_docs_do_arquivo(caminho_do_arquivo2)

#documentos_combinados = [combinar_linhas(doc1, doc2) for doc1, doc2 in zip(documentos1, documentos2)]
documentos_combinados = [construirDocumento(documentos1[i], documentos2[i]) for i in range(len(documentos1))]
print(documentos_combinados[0])
es = Elasticsearch(hosts=["http://localhost:9200"])

stream=(i for i in documentos_combinados)
for success, info in parallel_bulk(es, stream, chunk_size=500, thread_count=6, index="teste"):
    if not success:
        print('A document failed:', info)

# Verificar os resultados

