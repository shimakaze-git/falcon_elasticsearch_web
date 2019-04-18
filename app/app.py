# import os
import json
import falcon

from elasticsearch import Elasticsearch

es = Elasticsearch()


class IndexResource:
    def on_get(self, req, resp, **kwargs):
        msg = {
            'index': req.url,
            'search': req.url + "search/{index_name}"
        }
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(msg)


class SearcResource:

    def on_get(self, req, resp, **kwargs):
        if (
            ('word' in req.params) and (kwargs['index_name'] is not None)
        ):
            index_name = kwargs['index_name']
            word = req.params['word']

            _source = ['title', 'author']
            search_body = {
                '_source': _source,
                'size': 1000,
                'query': {
                    'match': {'text_kuromoji': word}
                }
            }

            # search process of elasticsearch
            res = es.search(index=index_name, body=search_body)
            hits = [
                dict(
                    list(doc['_source'].items()) + [('score', doc['_score'])]
                )
                for doc in res['hits']['hits']
            ]
            search_status = "search success"

            msg = {
                'search_word': word,
                'message': search_status,
                'hits': hits
            }
        else:
            msg = {
                'message': "word is not in parameter."
            }

        resp.body = json.dumps(msg)


class RedirectResource:
    def on_get(self, req, resp, **kwargs):
        redirect_url = "http://www.google.com"

        resp.status = falcon.HTTP_301
        resp.set_header('Location', redirect_url)


app = falcon.API()
app.add_route("/", IndexResource())
app.add_route("/search/{index_name}", SearcResource())
app.add_route("/redirect", RedirectResource())


if __name__ == "__main__":
    from wsgiref import simple_server
    httpd = simple_server.make_server("127.0.0.1", 8000, app)
    httpd.serve_forever()
