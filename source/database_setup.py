import os
from langchain_elasticsearch import ElasticsearchStore
from elasticsearch import Elasticsearch
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(api_key=os.environ.get("OPENAI_API_KEY"))


def setup_es_client() -> Elasticsearch:
    """
    Set up and return an Elasticsearch client using environment variables.

    This function reads the Elasticsearch API key and endpoint from environment variables,
    initializes an Elasticsearch client, and returns it.

    Returns:
        Elasticsearch: An initialized Elasticsearch client.
    """
    # Load environment variables for Elasticsearch API and endpoint
    ES_API = os.environ.get("ES_API")
    ES_ENDPOINT = os.environ.get("ES_ENDPOINT")

    # Initialize the Elasticsearch client
    es_client = Elasticsearch(
        ES_ENDPOINT,
        api_key=ES_API
    )

    return es_client


# Create the Elasticsearch client by calling the setup function
es_client = setup_es_client()


def setup_es_store(index_name: str, es_client: Elasticsearch):
    """
       Sets up and returns an ElasticsearchStore index for storing embeddings and for RAG.

       Args:
           index_name (str): The name of the Elasticsearch index where embeddings will be stored.
           es_client (Elasticsearch): An instance of the Elasticsearch client connected to the Elasticsearch cluster.

       Returns:
           ElasticsearchStore: An instance of ElasticsearchStore configured with the provided index name,
                                embeddings, and Elasticsearch connection.

       """
    es_vector_store = ElasticsearchStore(
        embedding=embeddings,
        index_name=index_name,
        es_connection=es_client
    )
    return es_vector_store

# Setup Elasticsearch store
es_store = setup_es_store("azal_activities", es_client)

