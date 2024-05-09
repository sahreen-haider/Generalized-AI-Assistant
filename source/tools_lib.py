import importlib
from langchain_core.tools import Tool

from logger import logging

class ToolFactory:
    @staticmethod
    def load_module(module_name: str):
        """Loads a Python dynamically based on its time.

        Args:
            module_name (str): The name of the module to load
            
        Returns:
            object: The loaded module.
            
        """
        try:
            return importlib.import_module(module_name)
        except ImportError as e:
            raise ImportError(f"Unable to load/import module '{module_name}': {str(e)}")


    @staticmethod
    def get_class_instance(module, class_name: str, settings: dict):
        """
        Retrieves an instance of a class from a module.

        Args:
            module: The module containing the class.
            class_name (str): The name of the class to retrieve.
            settings (dict): Settings to be passed to the class constructor.

        Returns:
            object: An instance of the specified class.
        """
        try:
            return getattr(module, class_name)(settings=settings)
        except AttributeError:
            raise ValueError(f"Class '{class_name}' not found in module '{module.__name__}'")
        
        
    @staticmethod
    def get_function(class_instance, function_name: str):
        """
        Retrieves a function from a class instance.

        Args:
            class_instance: An instance of a class.
            function_name (str): The name of the function to retrieve.

        Returns:
            function: The specified function.
        """
        if not hasattr(class_instance, function_name):
            raise ValueError(f"Function '{function_name}' not found in class '{class_instance.__class__.__name__}'")
        function = getattr(class_instance, function_name)
        if not callable(function):
            raise TypeError(f"Attribute '{function_name}' is not callable")
        return function

    @staticmethod
    def initialize_tool(tool_config: dict) -> Tool:
        """
        Initializes a tool based on the provided configuration.

        Args:
            tool_config (dict): Configuration for the tool.

        Returns:
            Tool: An instance of the initialized tool.
        """
        module = ToolFactory.load_module(tool_config["module"])
        if 'class' in tool_config:
            class_instance = ToolFactory.get_class_instance(module, tool_config['class'], tool_config)
            function = ToolFactory.get_function(class_instance, tool_config['function'])
        else:
            function = getattr(module, tool_config['function'])
            if not callable(function):
                raise TypeError(f"Function '{tool_config['function']}' is not callable")

        return Tool.from_function(func=function, name=tool_config['name'], description=tool_config.get('description'))


def initialize_tools(settings: dict) -> list:
    """
    Initializes a list of tools based on the provided settings.

    Args:
        settings (dict): The settings containing tool configurations.

    Returns:
        list: A list of initialized tools.
    """
    tools_list = []
    for tool_name, tool_config in settings["Tools"].items():
        try:
            tool = ToolFactory.initialize_tool(tool_config)
            tools_list.append(tool)
            logging.info(f"Tool {tool_name} initialized successfully.")  # Log successful initialization
        except Exception as e:
            logging.error(f"Error initializing tool {tool_name}: {str(e)}")  # Log error during initialization
    return tools_list
        
        