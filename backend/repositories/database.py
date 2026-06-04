import os
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from pymongo import MongoClient
from pymongo.errors import PyMongoError


def load_env_file() -> None:
    env_path = Path(__file__).resolve().parents[2] / ".env"
    if not env_path.exists():
        return

    for raw_line in env_path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


load_env_file()

def normalize_mongodb_uri(uri: str) -> str:
    if "mongodb+srv" not in uri:
        return uri

    parts = urlsplit(uri)
    query_params = dict(parse_qsl(parts.query, keep_blank_values=True))
    query_params.setdefault("tlsAllowInvalidCertificates", "true")
    query_params.setdefault("retryWrites", "true")
    query_params.setdefault("w", "majority")
    normalized_query = urlencode(query_params)

    return urlunsplit((parts.scheme, parts.netloc, parts.path, normalized_query, parts.fragment))


DEFAULT_MONGODB_URI = "mongodb://localhost:27017/"

MONGODB_URI = normalize_mongodb_uri(
    os.getenv("MONGODB_URI") or DEFAULT_MONGODB_URI
)

MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "habitplatform")
MONGODB_TIMEOUT_MS = int(os.getenv("MONGODB_TIMEOUT_MS", "5000"))

client = None
db = None


def get_database():
    global client, db
    if client is None or db is None:
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=MONGODB_TIMEOUT_MS)
        db = client[MONGODB_DB_NAME]
    return db


def ping_database() -> bool:
    try:
        current_client = client
        if current_client is None:
            get_database()
            current_client = client
        current_client.admin.command("ping")
    except PyMongoError:
        return False
    return True


def get_collection(name: str):
    return get_database()[name]
