from langchain_core.tools import tool
from search_tools import WebSearchTool 
from application.settings_manager import fetch_settings 


@tool 
def search_tool(question:str, app_id)->str:
    """This is a websearc tool that you can use for question about any website url"""
    settings= fetch_settings(app_id)
    web_search= WebSearchTool(settings)
    response= web_search.ws_tool(question)
    return response

# Putting all tools together
tools_list = [search_tool]