# =========================
# 📦 IMPORTS
# =========================

import boto3
import csv
import io
import hashlib
import logging

from opensearchpy import OpenSearch, helpers

# LangChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings


# =========================
# 🔐 CONFIG
# =========================

BUCKET = "itx-cdm-nas-epitcua"
SOURCE_PREFIX = "development/Adaptiv/depuy/processed_csvs/"
DONE_PREFIX = "development/Adaptiv/depuy/embedding_done/"
FAILED_PREFIX = "development/Adaptiv/depuy/embedding_failed/"

INDEX_NAME = "idx_depuy_vector_index"

# OpenSearch
OPENSEARCH_HOST = "https://your-opensearch-endpoint"
OPENSEARCH_USER = "YOUR_USERNAME"
OPENSEARCH_PASS = "YOUR_PASSWORD"

# Azure OpenAI
AZURE_API_KEY = "YOUR_KEY"
AZURE_ENDPOINT = "YOUR_ENDPOINT"
AZURE_API_VERSION = "2024-02-01"


# =========================
# 🔌 CLIENTS
# =========================

s3 = boto3.client("s3")

os_client = OpenSearch(
    hosts=[OPENSEARCH_HOST],
    http_auth=(OPENSEARCH_USER, OPENSEARCH_PASS),
    verify_certs=False
)

# LangChain Embedding
embedding_model = AzureOpenAIEmbeddings(
    api_key=AZURE_API_KEY,
    azure_endpoint=AZURE_ENDPOINT,
    api_version=AZURE_API_VERSION,
    model="text-embedding-3-large"
)

# LangChain Text Splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)


# =========================
# 🪵 LOGGING
# =========================

logging.basicConfig(
    filename="embedding_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# =========================
# 🆔 UNIQUE ID
# =========================

def generate_id(file_name, chunk_id):
    raw = f"{file_name}_{chunk_id}"
    return hashlib.md5(raw.encode()).hexdigest()


# =========================
# 📥 BULK INSERT
# =========================

def bulk_insert(actions):
    if actions:
        helpers.bulk(os_client, actions)


# =========================
# 📄 PROCESS CSV FILE
# =========================

def process_csv_file(key):
    print(f"Processing: {key}")
    logging.info(f"Processing file: {key}")

    obj = s3.get_object(Bucket=BUCKET, Key=key)


    # body = obj["Body"].read().decode("utf-8")
    # csv_reader = csv.DictReader(io.StringIO(body))


    # Streaming instead of loading whole file (if file size > 500mb then RAM may spike)
    stream = obj["Body"]
    csv_reader = csv.DictReader(
        (line.decode("utf-8") for line in stream)
    )

    actions = []
    failed_rows = 0

    for row_num, row in enumerate(csv_reader, start=1):
        try:
            file_name = row.get("file_name")
            content = row.get("content")

            if not content:
                continue

            # ✅ LangChain Chunking
            chunks = text_splitter.split_text(content)

            for i, chunk in enumerate(chunks):
                try:
                    # ✅ LangChain Embedding
                    embedding = embedding_model.embed_query(chunk)

                    doc_id = generate_id(file_name, i)

                    actions.append({
                        "_index": INDEX_NAME,
                        "_id": doc_id,
                        "_source": {
                            "file_name": file_name,
                            "content": chunk,
                            "embedding": embedding
                        }
                    })

                    # Bulk flush
                    if len(actions) >= 100:
                        bulk_insert(actions)
                        actions = []

                except Exception as e:
                    failed_rows += 1
                    logging.error(f"Chunk failed | File: {key} Row: {row_num} Error: {str(e)}")

        except Exception as e:
            failed_rows += 1
            logging.error(f"Row failed | File: {key} Row: {row_num} Error: {str(e)}")

    # Final flush
    bulk_insert(actions)

    return failed_rows


# =========================
# 📂 MOVE FILE
# =========================

def move_file(source_key, destination_prefix):
    dest_key = source_key.replace(SOURCE_PREFIX, destination_prefix)

    s3.copy_object(
        Bucket=BUCKET,
        CopySource={"Bucket": BUCKET, "Key": source_key},
        Key=dest_key
    )

    s3.delete_object(Bucket=BUCKET, Key=source_key)


# =========================
# 🔍 LIST FILES
# =========================

def list_csv_files():
    response = s3.list_objects_v2(Bucket=BUCKET, Prefix=SOURCE_PREFIX)

    files = []
    for obj in response.get("Contents", []):
        if obj["Key"].endswith(".csv"):
            files.append(obj["Key"])

    return files


# =========================
# 🚀 MAIN PIPELINE
# =========================

def run_pipeline():
    files = list_csv_files()

    print(f"Found {len(files)} CSV files")

    for file_key in files:
        try:
            failed_rows = process_csv_file(file_key)

            if failed_rows == 0:
                move_file(file_key, DONE_PREFIX)
                logging.info(f"SUCCESS: {file_key}")
            else:
                move_file(file_key, FAILED_PREFIX)
                logging.warning(f"PARTIAL FAILURE: {file_key} | Failed rows: {failed_rows}")

        except Exception as e:
            logging.error(f"FILE FAILED: {file_key} Error: {str(e)}")
            move_file(file_key, FAILED_PREFIX)


# =========================
# ▶️ RUN
# =========================

if __name__ == "__main__":
    run_pipeline()