from fastapi import FastAPI, HTTPException
from indexer.elastic_indexer import ElasticIndexer

app = FastAPI()
indexer = ElasticIndexer()

@app.get("/search")
def search(q: str):
    results = indexer.search(q)
    return [{"filename": r["filename"], "url": r["url"]} for r in results]
