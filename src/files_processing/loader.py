import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

pdf_files = [
    'trud.pdf',
    'trud_code.pdf'
]

all_documents = []

for pdf_path in pdf_files:
    loader = PyPDFLoader(
        file_path=pdf_path,
        extraction_mode='layout'
    )
    documents = loader.load()
    all_documents.extend(documents)

text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 100)
chunks = text_splitter.split_documents(all_documents)