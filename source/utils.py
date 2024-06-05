# Import the necessary libraries
import json
import os
from dotenv import load_dotenv
from langchain import hub
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_openai import ChatOpenAI

# Import local modules
from logger import logging
from exception import CustomException

os.environ.clear()

# Here we load the environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path)


def setup_model() -> object:
    """
    Initialize the large language model.

    Returns:
        object: A Large Language Model instance.
    """
    # Load the JSON string from the environment variable
    model_settings_str = os.environ.get("MODEL_SETTINGS")
    
    logging.info("Retrieved model settings string sucessfully: %s",
                 model_settings_str)
    

    # Parse the JSON string into a dictionary
    model_settings = json.loads(model_settings_str)
    
    # log the settings
    logging.info("Model settings loaded successfully", model_settings)

    # Create and configure the ChatOpenAI model instance
    llm_model = ChatOpenAI(
        model_name=model_settings.get('model_name'),
        streaming=model_settings.get('streaming'),
        callbacks=[StreamingStdOutCallbackHandler()],
        verbose=True
    )
    
    return llm_model


# Setup the model
model = setup_model()

def get_memory(session_id) -> object:
    """
    Retrieve conversational memory for a given session ID.

    This function retrieves the conversational memory associated with a specific session ID.
    The conversational memory contains the message history for the session stored in a Redis database.

    Args:
        session_id (str): The session ID for which memory is requested.

    Returns:
        object: Conversational Memory object.
    """
    logging.info("Retrieving conversational memory for session ID: ", session_id)

    # Create a RedisChatMessageHistory instance for storing message history
    redis_url = os.environ.get("REDIS_URL")
    message_history = RedisChatMessageHistory(url=redis_url, ttl=None, session_id=session_id)

    logging.info("Conversational memory retrieved successfully for session ID: %s", session_id)
    
    return message_history

def fetch_prompt(prompt_id) -> str:
    """
    Fetch a prompt from the Langchain hub.

    Args:
        prompt_id (str): The ID of the prompt to fetch.
    Returns:
        str: The fetched prompt.
    """
    prompt_hub= hub.pull(prompt_id)
    logging.info(f"fetched the prompt sucessfully {prompt_hub}")   
    return prompt_hub


import os
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from sklearn.cluster import KMeans
import numpy as np
from langchain_core.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain

from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain

from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(temperature=0,
                 model='gpt-3.5-turbo'
                )

# Get the Redis URL from the environment variable
redis_url = os.environ.get("REDIS_URL")

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ['SERPER_API_KEY'] = os.getenv('SERPER_API_KEY')


def summarize(id:str)->str:
    """
    Summarize the given id.
    """
    message_history = RedisChatMessageHistory(
        url=redis_url,
        session_id=id
        )
        
    message_history = str(message_history)  
    text = ''
    
    # for i, page in enumerate(pdfreader.pages):
    for page in message_history:
        text += page
        
    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", "\t"], chunk_size=10000, chunk_overlap=50)

    docs = text_splitter.create_documents([text])
    embeddings = OpenAIEmbeddings()

    vectors = embeddings.embed_documents([x.page_content for x in docs])
    
    num_clusters = 1

    # Perform K-means clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init='auto').fit(vectors)
    # Find the closest embeddings to the centroids

    # Create an empty list that will hold your closest points
    closest_indices = []

    # Loop through the number of clusters you have
    for i in range(num_clusters):
        
        # Get the list of distances from that particular cluster center
        distances = np.linalg.norm(vectors - kmeans.cluster_centers_[i], axis=1)
        
        # Find the list position of the closest one (using argmin to find the smallest distance)
        closest_index = np.argmin(distances)
        
        # Append that position to your closest indices list
        closest_indices.append(closest_index)
        
    selected_indices = sorted(closest_indices)
    
    map_prompt = """
        You will be given a document.
        Your goal is to extract all the human questions and give a summary of this human questions so that a reader will have a full understanding of what happened.
        Your response should be precise and according to what was said in the passage.

        ```{text}```
        FULL SUMMARY:
        """
    map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text"])
    
    # map_chain = load_summarize_chain(llm=llm,
    #                          chain_type="stuff",
    #                          prompt=map_prompt_template)
    
    llm_chain = LLMChain(llm=llm, prompt=map_prompt_template)
    
    map_chain = StuffDocumentsChain(llm_chain=llm_chain,
                             document_variable_name="text",
                             )
    
    selected_docs = [docs[doc] for doc in selected_indices]
    
    # Make an empty list to hold your summaries
    summary_list = []

    # Loop through a range of the lenght of your selected docs
    for i, doc in enumerate(selected_docs):
        
        # Go get a summary of the chunk
        chunk_summary = map_chain.invoke([doc])
        
        # Append that summary to your list
        summary_list.append(chunk_summary)
        
    return chunk_summary['output_text']

# summarize("123")


# Testing the code
# if __name__ == "__main__":
#     fetch_prompt()
    