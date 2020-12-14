import os

MONGO_URI = os.getenv("MONGO_URI")
MINIO_HOST = os.getenv("MINIO_HOST")
MINIO_PORT = os.getenv("MINIO_PORT")
MINIO_BUCKET = os.environ.get("MINIO_BUCKET")
MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY")

DB_NAME = os.getenv("DB_NAME", "law_data")
COLLECTION_NAME = os.getenv("URL_DB_NAME", "pdf_data")
ENTRYURL = "https://law.moj.gov.tw/Law/LawSearchLaw.aspx"
INVALID_CATEGORIES = ["憲法"]
URL_PREFIX = "https://law.moj.gov.tw"
DOWNLOAD_PATH = "pdf_data"
DOWNLOAD_URL = "https://law.moj.gov.tw/LawClass/FilesType.aspx?DataId={}&SLI=CALL"
