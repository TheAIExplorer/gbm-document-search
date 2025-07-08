from cloud_connectors.google_drive import GoogleDriveConnector
from document_parser.parser_factory import ParserFactory
from indexer.elastic_indexer import ElasticIndexer
from models.document import Document

def main():
    connector = GoogleDriveConnector()
    parser_factory = ParserFactory()
    indexer = ElasticIndexer()
    
    # Fetch current files from Google Drive
    files = connector.fetch_supported_files()
    current_file_ids = set(meta['id'] for meta in files)

    # Fetch all indexed documents
    try:
        indexed_docs = indexer.es.search(index=indexer.INDEX, body={"query": {"match_all": {}}}, size=10000)
        indexed_file_ids = set(doc['_id'] for doc in indexed_docs['hits']['hits'])
    except Exception:
        indexed_file_ids = set()

    # Delete documents from index that are no longer in Google Drive
    for file_id in indexed_file_ids - current_file_ids:
        indexer.delete_document(file_id)

    # Index or update current files
    for meta in files:
        path = connector.download_file(meta)
        parser = parser_factory.get_parser(path)
        text = parser.extract_text(path)
        doc = Document(meta['id'], meta['name'], text, meta['webViewLink'])
        indexer.index_document(doc)
    
    print("Indexing and sync done.")

if __name__ == "__main__":
    main()
