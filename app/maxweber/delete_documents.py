# import os
from elasticsearch import Elasticsearch

dirname = "./documents"

es = Elasticsearch()

index_name = 'max_weber'
es.indices.delete(index=index_name)
