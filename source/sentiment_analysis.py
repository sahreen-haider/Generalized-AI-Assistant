from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from dotenv import load_dotenv
from langchain_community.chat_message_histories import RedisChatMessageHistory

import os

load_dotenv()

# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("text-classification", model="Dmyadav2001/Sentimental-Analysis")

# Get the Redis URL from the environment variable
redis_url = os.environ.get("REDIS_URL")
os.environ['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY')

def get_sentiment(id:str):

    message_history = RedisChatMessageHistory(
            url=redis_url,
            session_id=id
            )
    message_history = str(message_history)
    prompt = """Analyze the sentiment of the following user query 
                and provide a brief description of the sentiment:
    {text}"""
    sentiment_prompt = PromptTemplate.from_template(prompt)

    # llm = OpenAI(temperature=0.5)
    llm = pipe

    chain = (
        sentiment_prompt | llm
    )

    result = chain.invoke({"text": message_history})
    print(result)
    return result
# print(result)

if __name__ == '__main__':
    get_sentiment("123asd")