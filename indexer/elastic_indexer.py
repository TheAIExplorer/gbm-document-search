from elasticsearch import Elasticsearch
from models.document import Document
from utils.config import ELASTIC_HOST

class ElasticIndexer:
    INDEX = "docs"

    def __init__(self):
        # Connect to Elasticsearch with SSL and basic auth
        self.es = Elasticsearch(
            ELASTIC_HOST
        #     basic_auth=("elastic", "changeme"),  # Default password, change if needed
        #     ca_certs="elasticsearch-9.0.3-windows-x86_64/elasticsearch-9.0.3/config/certs/http_ca.crt",
        #     verify_certs=True
        )
        if not self.es.indices.exists(index=self.INDEX):
            self.es.indices.create(index=self.INDEX, body={
              "mappings": {
                "properties": {"file_id": {"type": "keyword"}, "filename": {"type": "text"}, "content": {"type": "text"}, "url": {"type": "keyword"}}
              }
            })

    def index_document(self, doc: Document):
        self.es.index(index=self.INDEX, id=doc.file_id, body=doc.__dict__)

    def delete_document(self, file_id: str):
        self.es.delete(index=self.INDEX, id=file_id, ignore=[404])

    def search(self, query: str):
        resp = self.es.search(index=self.INDEX, body={"query": {"multi_match": {"query": query, "fields": ["content", "filename"]}}})
        return [hit["_source"] for hit in resp["hits"]["hits"]]
