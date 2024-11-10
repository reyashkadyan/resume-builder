# Resume and Cover Letter Builder with RAG-based Knowledge Base

This project provides a comprehensive solution for generating a tailored resume and cover letter using a knowledge base. It allows you to create personalized cover letters by using a combination of your resume and project experience, indexed for efficient retrieval, following the RAG (Retrieval-Augmented Generation) pipeline principles.

## Setup Instructions

### 1. Add Your OpenAI API Key
This project relies on OpenAI’s language models, so you’ll need to set up your OpenAI API key.

- First, [sign up](https://platform.openai.com/signup) and get an API key from OpenAI.
- Set your API key as an environment variable:

  - On **macOS/Linux**:
    ```bash
    export OPENAI_API_KEY="your_openai_api_key"
    ```

  - On **Windows** (Command Prompt):
    ```cmd
    set OPENAI_API_KEY="your_openai_api_key"
    ```

  - **Alternatively**: Use a `.env` file by creating one in the root of your project with the following contents:

    ```env
    OPENAI_API_KEY="your_openai_api_key"
    ```

    Then install `python-dotenv` to load it:

    ```bash
    pip install python-dotenv
    ```

### 2. Add Your Resume Content

Add a file with the content of your resume in markdown format to the `content` folder, saving it as a `.txt` file. Make sure the content is formatted properly, as this will be used to generate your final resume.

- Example: `content/sample_resume_markdown.txt`

### 3. Add Project Experience Content

Add a file with a detailed description of your project experience. Include information about project objectives, technical details, accomplishments, etc. This file should also be saved in the `content` folder as a `.txt` file.

- Example: `content/sample_project_experience.txt`

### 4. Add the Job Description

To tailor a cover letter using your resume and project experience, add the job description you want to apply for as a `.txt` file in the `content` folder. Ensure each point is formatted with a bullet `-` to separate each requirement clearly.

- Example: `content/sample_job_description.txt`

### 5. Run the Scripts

With your environment and content files prepared, you can run the scripts to generate your resume, build an index for the RAG pipeline, and create a cover letter.

#### a. Generate a Formatted Resume

To format your resume from the markdown content, run the following command:

```bash
python -m src.scripts.resume_builder
```

This script will generate a formatted resume in the `files` directory based on your markdown content.

#### b. Create the Knowledge Base Index

To create an index of your resume and project experience, which serves as the knowledge base for the RAG pipeline, run:

```bash
python -m src.scripts.create_rag_index
```

This script indexes your resume and project content for efficient retrieval, storing the index file and metadata in the `data` folder.

#### c. Generate a Cover Letter

To generate a tailored cover letter using the job description, your resume, and project experience, run the following command:

```bash
python -m src.scripts.cover_letter_builder
```

This script will create a personalized cover letter and save it in the `letters` folder.

---

## Project Structure

```
resume_builder/
├── content/                       # Contains input text files
│   ├── sample_resume_markdown.txt
│   ├── sample_project_experience.txt
│   └── sample_job_description.txt
├── data/                          # Stores generated FAISS index files and metadata
│   ├── sample_cosine_index.idx
│   ├── sample_cosine_index_metadata.csv
│   ├── sample_hnsw_index.idx
│   └── sample_hnsw_index_metadata.csv
├── files/                         # Contains generated resume PDFs
│   └── Sample_Resume.idx
├── letters/                       # Contains generated cover letters
│   └── Sample_Cover_Letter.idx
├── src/
│   ├── scripts/                   # Scripts to generate resume, index, and cover letter
│   └── utils/                     # Utility functions for text extraction and chunking
└── requirements.txt               # Python dependencies
```

---

## Dependencies

Install the dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## Important Notes

- **API Key Security**: For security, it’s recommended to avoid hardcoding the API key in scripts. Instead, use environment variables or a `.env` file.
- **Index Files**: The generated FAISS index files are saved in the `data` directory and will be used in the RAG pipeline.
- **Content Format**: Ensure that all text files in `content` are formatted correctly, as the script relies on consistent structure to parse and process the content.

---