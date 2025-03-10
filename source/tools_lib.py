import sys

# Adding paths to import custom modules
sys.path.insert(1, "source")
sys.path.insert(2, "application")
sys.path.insert(3, "configuration")

from langchain_core.tools import tool
from source.search_tools import WebSearchTool
from application.settings_manager import fetch_settings

from database_setup import es_store

@tool
def search_tool_wildfloc(question: str):
    """This is a websearch tool that you can use for question about any website url"""
    settings = fetch_settings("wildfloc")
    web_search = WebSearchTool(settings)
    response = web_search.wb_tool(question)
    return response

@tool
def search_tool_jordan(question: str):
    """This is a websearch tool that you can use for question about any website url"""
    settings = fetch_settings("jordan")
    web_search = WebSearchTool(settings)
    response = web_search.wb_tool(question)
    return response

@tool
def azal_database_tool(question:str):
    """
    Fetch general activities based on a query from Elasticsearch store and process the response.
    """
    docs = es_store.as_retriever().invoke(question)
    return docs

@tool
def CQAI_tool(question:str):
    """This is a websearch tool that you can use for question about any website url"""
    settings = fetch_settings("jordan")
    web_search = WebSearchTool(settings)
    response = web_search.wb_tool(question)
    return response


# Putting all tools together
# tools_list_wildfloc = [search_tool_wildfloc]
tools_list_jordan = [CQAI_tool]

