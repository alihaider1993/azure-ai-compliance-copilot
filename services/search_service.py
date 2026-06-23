import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    VectorSearchProfile,
    HnswAlgorithmConfiguration,
)
from azure.core.credentials import AzureKeyCredential

load_dotenv()

AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX")
AZURE_SEARCH_ADMIN_KEY = os.getenv("AZURE_SEARCH_ADMIN_KEY")

EMBEDDING_DIMENSIONS = 1536


def get_search_credential():
    if AZURE_SEARCH_ADMIN_KEY:
        return AzureKeyCredential(AZURE_SEARCH_ADMIN_KEY)
    return DefaultAzureCredential()


def get_search_client():
    return SearchClient(
        endpoint=AZURE_SEARCH_ENDPOINT,
        index_name=AZURE_SEARCH_INDEX,
        credential=get_search_credential(),
    )


def get_index_client():
    return SearchIndexClient(
        endpoint=AZURE_SEARCH_ENDPOINT,
        credential=get_search_credential(),
    )


def create_index():
    index_client = get_index_client()

    fields = [
        SimpleField(
            name="id",
            type=SearchFieldDataType.String,
            key=True,
        ),
        SearchableField(
            name="file_name",
            type=SearchFieldDataType.String,
        ),
        SearchableField(
            name="chunk_text",
            type=SearchFieldDataType.String,
        ),
        SimpleField(
            name="page_number",
            type=SearchFieldDataType.Int32,
            filterable=True,
        ),
        SimpleField(
            name="source_type",
            type=SearchFieldDataType.String,
            filterable=True,
            facetable=True,
        ),
        SimpleField(
            name="framework",
            type=SearchFieldDataType.String,
            filterable=True,
            facetable=True,
        ),
        SearchField(
            name="embedding",
            type=SearchFieldDataType.Collection(
                SearchFieldDataType.Single
            ),
            searchable=True,
            vector_search_dimensions=EMBEDDING_DIMENSIONS,
            vector_search_profile_name="vector-profile",
        ),
    ]

    vector_search = VectorSearch(
        algorithms=[
            HnswAlgorithmConfiguration(
                name="hnsw-config",
            )
        ],
        profiles=[
            VectorSearchProfile(
                name="vector-profile",
                algorithm_configuration_name="hnsw-config",
            )
        ],
    )

    index = SearchIndex(
        name=AZURE_SEARCH_INDEX,
        fields=fields,
        vector_search=vector_search,
    )

    result = index_client.create_or_update_index(index)
    print(f"Index created: {result.name}")


def upload_documents(documents: list[dict]):
    search_client = get_search_client()
    result = search_client.upload_documents(documents)
    return result


def vector_search(query_vector: list[float], top: int = 7):
    search_client = get_search_client()

    results = search_client.search(
        search_text=None,
        vector_queries=[
            {
                "kind": "vector",
                "vector": query_vector,
                "fields": "embedding",
                "k": top,
            }
        ],
        select=[
            "id",
            "file_name",
            "chunk_text",
            "page_number",
            "source_type",
            "framework",
        ],
        top=top,
    )

    return [dict(result) for result in results]