import os
import sys

import re
import pandas as pd
import numpy as np

import faiss

from sentence_transformers import SentenceTransformer

from src.utils.extactors import extract_text_from_text_file, extract_text_from_pdf_file
from src.utils.chunkers import block_chunk

# Model to create text embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

def save_faiss_hnsw_index(embeddings, metadata, index_filename="./data/sample_hnsw_index.idx", metadata_filename="./data/sample_hnsw_index_metadata.csv"):
    # Embeddings and metadata
    embedding_matrix = np.array(embeddings).astype("float32")
    metadata_df = pd.DataFrame(metadata)

    # Create HNSW Index
    embedding_dimension = embedding_matrix.shape[1]
    M  =  32 # Number of neighbors in the graph
    hnsw_index = faiss.IndexHNSWFlat(embedding_dimension, M, faiss.METRIC_INNER_PRODUCT)
    # hnsw_index.hnsw.M = 32  
    hnsw_index.hnsw.efConstruction = 200  # Higher values increase index accuracy (construction time vs. recall)
    hnsw_index.add(embedding_matrix)

    faiss.write_index(hnsw_index,index_filename)
    metadata_df.to_csv(metadata_filename, index=False)
    print("FAISS HNSW index and metadata saved locally.")

def save_faiss_cosine_index(embeddings, metadata, index_filename="./data/sample_cosine_index.idx", metadata_filename="./data/sample_cosine_index_metadata.csv"):
    # Embeddings and metadata
    embedding_matrix = np.array(embeddings)
    metadata_df = pd.DataFrame(metadata)

    # Create FAISS index
    embedding_dimension = embedding_matrix.shape[1]
    index = faiss.IndexFlatIP(embedding_dimension)  # IndexFlatL2 for euclidean distance; IndexFlatIP for cosine similarity
    index.add(embedding_matrix)

    faiss.write_index(index, index_filename)
    metadata_df.to_csv(metadata_filename, index=False)
    print("FAISS Cosine index and metadata saved locally.")

def create_index(txt_files, pdf_files, type='hnsw'):
    '''
    Parameters:
    - txt_files: List object containing path of text files to index.
    - pdf_files: List object containing path of PDF files to index.
    - type: Type of index to save. `cosine` or `hnsw` accepted.
    '''

    metadata = []
    embeddings = []

    # Function to extract chunks from the documents to index
    def process_chunks(chunks, doc_type):
        for i, chunk in enumerate(chunks):
            embedding = model.encode(chunk)
            embeddings.append(embedding)
            metadata.append({
                "doc_type": doc_type,
                "chunk_num": i,
                "text": chunk,
    })
            
    if len(txt_files)>0:
        txt_files_parsed = [extract_text_from_text_file(txt_file) for txt_file in txt_files]
        txt_files_chunked = [block_chunk(txt_file) for txt_file in txt_files_parsed]
        for idx, txt_chunks in enumerate(txt_files_chunked):
            process_chunks(txt_chunks, txt_files[idx].split('/')[-1].split('.')[0])

    if len(pdf_files)>0:     
        pdf_files_parsed = [extract_text_from_pdf_file(pdf_file) for pdf_file in pdf_files]
        pdf_files_chunked = [block_chunk(pdf_file) for pdf_file in pdf_files_parsed]
        for idx, pdf_chunks in enumerate(pdf_files_chunked):
            process_chunks(pdf_chunks, pdf_files[idx].split('/')[-1].split('.')[0])

    if type=='cosine':
        save_faiss_cosine_index(embeddings, metadata)
    else:
        save_faiss_hnsw_index(embeddings, metadata)

if __name__=="__main__":

    RESUME_PDF_FILE_PATH = "./files/Sample_Resume.pdf"
    RESUME_TEXT_FILE_PATH = "./content/sample_resume_markdown.txt"
    PROJECT_EXPERIENCE_TEXT_FILE_PATH = "./content/sample_project_experience.txt"

    TXT_FILES = [PROJECT_EXPERIENCE_TEXT_FILE_PATH]
    PDF_FILES = [RESUME_PDF_FILE_PATH]
    create_index(txt_files=TXT_FILES, pdf_files=PDF_FILES, type='cosine')