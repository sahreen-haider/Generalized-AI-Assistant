from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY')


prompt = """Analyze the sentiment of the following text with few words of description:
{text}"""
sentiment_prompt = PromptTemplate.from_template(prompt)

llm = OpenAI(temperature=0.5)

print(f'Default model is: {llm.model_name}')

chain = (
    sentiment_prompt | llm
)

result = chain.invoke({"text": "I miss you, but its clear that you are having the time of your life."})
print(result)