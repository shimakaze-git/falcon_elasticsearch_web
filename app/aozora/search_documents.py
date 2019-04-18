from elasticsearch import Elasticsearch

es = Elasticsearch()

# 登録したデータからaliceを含むタイトルを検索してみる
source = ['title', 'author']
# source = ['title']

index_name = 'aozora'
# search_text = '夏目'
search_text = 'こころ'
body = {
    '_source': source,
    'query': {
        'match': {
            # 'text': search_text,
            'text_kuromoji': search_text
        }
    }
}
res = es.search(index=index_name, body=body)
hits_total_count = res['hits']['total']

print("検索ヒット数 : {}".format(hits_total_count))

for doc in res['hits']['hits']:
    print(doc['_source'])
