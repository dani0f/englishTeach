import json
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# Load API key from credentials file
with open("credentials.json", "r") as f:
    api = json.load(f)
    key = api["openai"]

# Initialize message history
message_history = []

def askTeacher(ask):
    chat = ChatOpenAI(openai_api_key=key)
    
    # Initial system message to set the context (if message history is empty)
    if not message_history:
        initial_prompt = (
            "This is a transcribed text from a customer's audio order in a restaurant. "
            "Your task is to interpret this order, clearly identify the dishes, drinks, and any additional instructions "
            "(such as ingredient changes, cooking specifications, or preferences). "
            "If there are transcription errors or unclear phrases, use the context to deduce the intent. "
            "Return the order structured as a clear list of dishes and drinks, including the customer's additional notes."
        )
        message_history.append(SystemMessage(content=initial_prompt))
    
    # Add the new human message to the message history
    message_history.append(HumanMessage(content=ask))
    
    # Send the message history to the chat model
    response = chat(message_history)
    
    # Append the model's response to the message history
    message_history.append(SystemMessage(content=response.content))
    
    # Return the model's response content
    return response.content
