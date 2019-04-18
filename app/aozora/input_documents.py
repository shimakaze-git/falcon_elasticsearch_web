import os
from elasticsearch import Elasticsearch

dirname = "./documents"

es = Elasticsearch()


# document投入
def insert_document(title=str, author=str, text=str, id=int):
    doc = {
        'text_kuromoji': text,
        'text_cjk': text,
        'title': title,
        'author': author
    }
    es.index(index='aozora', doc_type='aozora', id=id+1, body=doc)


for id, fname in enumerate(os.listdir(dirname)):
    # パース周り
    text, title, author = '', '', ''

    with open(os.path.join(dirname, fname), 'rt') as f:
        for row_num, line in enumerate(f):
            if row_num > 2:
                text += line
            elif row_num == 0:
                title = line.strip()
            elif row_num == 1:
                author = line.strip()

    print(author, title)

    # documentの導入
    insert_document(title, author, text, id)
