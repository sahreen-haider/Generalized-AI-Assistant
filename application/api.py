import sys

import uvicorn
from fastapi import FastAPI, HTTPException

# Adding paths to import custom modules
sys.path.insert(1, "source")
sys.path.insert(2, "application")
sys.path.insert(3, "configuration")

# Importing input schemas
from schemas import QueryInput, SettingsInput, SummarizeRequest

# Importing functions to fetch and update settings
from settings_manager import fetch_settings, insert_settings

# Importing the main function to execute the agent
from source.ast_main import execute_agent
from source.utils import summarize

# Creating a FastAPI instance
app = FastAPI()

@app.post("/invoke/{app_id}")
async def invoke_agent(app_id: str, query_input:QueryInput) -> dict:
    """
        Endpoint to invoke the agent driver function using the app_id and input parameters.

        Args:
            app_id (str): The name of the application.
            query_input (QueryInput): Input parameters including session_id and query.

        Returns:
            dict: Result returned by the agent.
        """
    in_params= {"app_name": app_id, "session_id": query_input.session_id, "query": query_input.query}
    try:
        settings= fetch_settings(app_id)
        if settings is None:
            raise HTTPException(status_code=404, detail="Settings not found")
        result= execute_agent(in_params, settings)
        return {"result": result}
    except Exception as e:
        print("Loged here")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/settings/{app_id}")
async def update_settings(app_id: str, settings_input: SettingsInput) -> dict:
    try:
        insert_settings(app_id, settings_input.settings)
        return {"message": "settings inserted sucessfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/settings/{app_id}")
async def get_settings(app_id: str) -> dict:
    try:
        settings= fetch_settings(app_id)
        return settings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




# Define the API endpoint
@app.post("/summarize/")
def summarize_endpoint(request: SummarizeRequest):
    try:
        summary = summarize(request.session_id)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))