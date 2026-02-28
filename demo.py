import json
from ollama import chat

# remember to run 'brew services start ollama' 
# then run 'ollama run llama3.2' in a separate terminal 

print('testing')
response = chat(model='llama3.2', messages=[
    {
        'role': 'user',
        'content': 'Why is the sky blue?',
    },
])
print(response.message.content)