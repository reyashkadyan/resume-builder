import os
import pandas as pd
import numpy as np

import openai
from openai import OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

import faiss

from sentence_transformers import SentenceTransformer

from src.utils.query import query_faiss_hnsw_index, query_faiss_cosine_index

def main():

    JOB_DESCRIPTION_FILE_PATH = "./content/sample_job_description.txt"
    INDEX_FILE_PATH = "./data/sample_cosine_index.idx"
    METADATA_FILE_PATH = "./data/sample_cosine_index_metadata.csv"
    COVER_LETTER_FILE_PATH = "./letters/Sample_Cover_Letter.txt"

    model = SentenceTransformer('all-MiniLM-L6-v2')

    with open(JOB_DESCRIPTION_FILE_PATH, "r") as job_description_file:
        job_description = job_description_file.read()

    job_description_points = [txt.strip() for txt in job_description.split('- ') if len(txt.strip())>1]

    # Extract relevant experience to the job description points
    relevant_experience = []
    for point in job_description_points:
        relevant_experience_txt = query_faiss_cosine_index(
            model,
            point,
            INDEX_FILE_PATH,
            METADATA_FILE_PATH,
            k=1)
        relevant_experience.append(relevant_experience_txt)

    relevant_experience_points = dict(zip(list(zip(range(1, len(job_description_points)+1), job_description_points)), relevant_experience))
    relevant_experience_points_str = "\n".join([f"{key[0]}. {key[1]}: {value}" for key, value in relevant_experience_points.items()])

    # Reading cover letter builder prompt
    with open("./content/cover_letter_prompt.txt", "r") as file:
        cover_letter_prompt = file.read()
    cover_letter_prompt = cover_letter_prompt.format(relevant_experience_points_str=relevant_experience_points_str)

    # Query OpenAI API
    client = OpenAI()
    response = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": cover_letter_prompt,
        }],
        model="gpt-4o-mini",
    )
    response_text = response.choices[0].message.content

    # Saving customised cover letter
    with open(COVER_LETTER_FILE_PATH, "w+") as file:
        file.write(response_text)
    print(f"Cover letter saved to {COVER_LETTER_FILE_PATH}")


if __name__=="__main__":
    main()