from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

openai = ChatOpenAI(model='gpt-6-luna')