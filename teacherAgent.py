import json
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from getMenuSting import getMenu

# Load API key from credentials file
with open("credentials.json", "r") as f:
    api = json.load(f)
    key = api["openai"]

# Initialize message history
message_history = []

def askTeacher(ask):
    chat = ChatOpenAI(openai_api_key=key)
    
    # Initial system message to set the context (if message history is empty)
    # Initial system message to set the context (if message history is empty)
    if not message_history:
        initial_prompt = (
            f"This is a transcribed text from a customer's audio order in a restaurant. "
            f"Your task is to interpret this order, clearly identify the dishes, drinks, and any additional instructions "
            f"(such as ingredient changes, cooking specifications, or preferences). "
            f"The available menu items are: {getMenu()}. "
            f"If there are transcription errors or unclear phrases, use the context to deduce the intent. "
            f"Only select items from the provided menu. "
            f"Return a structured JSON with a 'message' and 'items'. If no valid items are found, return the following: "
            f'{{"message": "no items", "items": []}}. '
            f"If there are valid items, return the following structure with a message: "
            f'{{"message": "items found", "items": [{{\n'
            f'    "id": "21a6e623-70e4-4a0f-b25d-cf9130af31a4",\n'
            f'    "Name": "Mojito",\n'
            f'    "Description": "Refreshing cocktail with mint, lime, and soda water.",\n'
            f'    "Price": "800",\n'
            f'    "Tags": ["beverage", "cocktail", "contains alcohol"],\n'
            f'    "Picture URL": "https://example.com/images/mojito.jpg",\n'
            f'    "quantity": "1"\n'
            f'}}]}}'
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
