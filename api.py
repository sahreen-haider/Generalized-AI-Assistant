import sys

import uvicorn
from fastapi import FastAPI, HTTPException

# Adding paths to import custom modules
sys.path.insert(1, "source")
sys.path.insert(2, "application")
sys.path.insert(3, "configuration")

# Importing input schemas
from application.schemas import QueryInput, SettingsInput

# Importing functions to fetch and update settings
from application.settings_manager import fetch_settings, insert_settings

# Importing the main function to execute the agent
from source.ast_main import execute_agent

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
        print("triyng to pront setting \n")
        settings= fetch_settings(app_id)
        print(settings)
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


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)