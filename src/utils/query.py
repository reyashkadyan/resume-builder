import faiss
import pandas as pd

def query_faiss_hnsw_index(model, query, index_file, metadata_file, k=1):
    hnsw_index = faiss.read_index(index_file)
    metadata_df = pd.read_csv(metadata_file)

    # Perform a query
    query_embedding = model.encode(query).astype("float32").reshape(1, -1)

    # Set the search parameter for higher recall at query time
    hnsw_index.hnsw.efSearch = 50  # Higher values give better recall (adjust based on dataset size)

    # Search
    distances, indices = hnsw_index.search(query_embedding, k)

    # Retrieve corresponding metadata
    results = metadata_df.iloc[indices[0]].reset_index()
    return '\n'.join(results['text'].to_list())

def query_faiss_cosine_index(model, query, index_file, metadata_file, k=1):
    faiss_index = faiss.read_index(index_file)
    metadata_df = pd.read_csv(metadata_file)

    # Perform a query
    query_embedding = model.encode(query).astype("float32").reshape(1, -1)

    # Search
    distances, indices = faiss_index.search(query_embedding, k)

    # Retrieve corresponding metadata
    results = metadata_df.iloc[indices[0]].reset_index()
    return '\n'.join(results['text'].to_list())