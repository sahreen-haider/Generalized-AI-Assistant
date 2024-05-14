from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.runnables.history import RunnableWithMessageHistory

from tools_lib import tools_list
from utils import model, get_memory, fetch_prompt
from logger import logging

class AgentManager:
    def __init__(self, settings: dict):
        """
        Initializes the AgentManager with the given settings.

        Args:
            settings (dict): Dictionary containing settings for the agent.
        
        """
        self.settings = settings
        
    def initialize_agent(self) -> RunnableWithMessageHistory:
        """
        Initializes and configures the agent for execution.

        Returns:
            RunnableWithMessageHistory: An agent runnable with message history.
        """
        # Fetch prompt based on settings
        prompt_id = self.settings["parent_settings"]["agent_id"]
        prompt = fetch_prompt(prompt_id)
        
        # Initialize tools required for agent execution
        # tools_list = initialize_tools(self.settings)
        
        logging.info("Initializing tools successfully")

        # Create an agent using OpenAI tools
        agent = create_openai_tools_agent(model, tools_list, prompt)

        # Create an AgentExecutor for executing the agent
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools_list,
            verbose=True,
            return_intermediate_steps=True,
            early_stopping_method="generate"
        )

        # Wrap the agent executor with message history functionality
        agent_with_history = RunnableWithMessageHistory(
            agent_executor,
            lambda session_id: get_memory(session_id),
            input_messages_key="input",
            history_messages_key="chat_history"
        )
        logging.info("Agent initialized successfully")

        return agent_with_history
    
    
def execute_agent(in_params: dict, settings: dict):
    """
    Executes the agent using the provided input parameters and settings.

    Args:
        in_params (dict): Input parameters for the agent execution.
        settings (dict): Settings required for agent initialization and execution.

    Returns:
        str: Result of the agent execution.
    """
    session_id = in_params["session_id"]

    # Initialize AgentManager with provided settings
    agent_manager = AgentManager(settings=settings)

    try:
        # Initialize and configure the agent
        agent = agent_manager.initialize_agent()

        # Invoke the agent with input parameters
        result = agent.invoke({
            "input": in_params["query"]
        }, {
            'configurable': {
                'session_id': session_id
            }
        })
        result = result["output"]
    except Exception as e:
        print(f"Error during agent execution: {e}")
        # Return an error message in case of exception
        result = "Internal Error, If the issue persists please call admin"

    return result
