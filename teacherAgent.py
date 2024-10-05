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
    promp = (f"This is a transcribed text from a customer's audio order in a restaurant. "
                              f"Your task is to interpret this order, clearly identify the dishes, drinks, and any additional instructions "
                              f"(such as ingredient changes, cooking specifications, or preferences). "
                              f"If there are transcription errors or unclear phrases, use the context to deduce the intent. "
                              f"Return the order structured as a clear list of dishes and drinks, including the customer's additional notes.")
    messages = [
        SystemMessage(content=promp),
        HumanMessage(content=ask)
    ]
    return chat(messages).content
 





