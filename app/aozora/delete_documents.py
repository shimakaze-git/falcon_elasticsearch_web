# import os
from elasticsearch import Elasticsearch

dirname = "./documents"

es = Elasticsearch()

index_name = 'aozora'
es.indices.delete(index=index_name)
