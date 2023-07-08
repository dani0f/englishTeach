import json
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage,
    SystemMessage
)

with open("credentials.json", "r") as f:
    api = json.load(f)
    key = api["openai"]

def askTeacher(ask):
    chat = ChatOpenAI(openai_api_key=key)
    promp = """"You are a friendly professional English teacher.
    Your job is to identify and describe coherence errors in the text. 
    For indicate a error you start with "You have a error:".
    If is not error you say "Congrats, the sentence is correct".
    The text is only in english, do not use another language.
    """
    messages = [
        SystemMessage(content=promp),
        HumanMessage(content=ask)
    ]
    return chat(messages).content
 



