from azure.identity import DefaultAzureCredential
from azure.cosmos import CosmosClient
from utils.config import COSMOS_ENDPOINT, COSMOS_DATABASE_NAME

credential = DefaultAzureCredential()

cosmos_client = CosmosClient(
    COSMOS_ENDPOINT,
    credential=credential,
)

database = cosmos_client.get_database_client(COSMOS_DATABASE_NAME)

documents_container = database.get_container_client("documents")
reviews_container = database.get_container_client("reviews")
findings_container = database.get_container_client("findings")
reports_container = database.get_container_client("reports")
audit_logs_container = database.get_container_client("audit_logs")


def upsert_item(container_name: str, item: dict) -> dict:
    container_map = {
        "documents": documents_container,
        "reviews": reviews_container,
        "findings": findings_container,
        "reports": reports_container,
        "audit_logs": audit_logs_container,
    }

    return container_map[container_name].upsert_item(item)