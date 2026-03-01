import json
from ollama import chat

# requires ollama to be installed and running
# remember to run 'brew services start ollama' 
# then run 'ollama run llama3.2' in a separate terminal 

def run_prompt_test(prompt_file: str):
    with open(prompt_file, 'r') as f:
        prompts = json.load(f)


    for prompt in prompts['prompts']:
        
        response = chat(model='llama3.2', messages=[
            {
                'role': 'user',
                'content': prompt['prompt'],
            },
        ])
        print(response.message.content)

        prompt['response'] = response.message.content

    with open(prompt_file, 'w') as f:
        json.dump(prompts, f, indent=4)


def main():
    
    #violent content prompts, all should be refused
    run_prompt_test('vt_prompts.json')
    
    #weapon content prompts, all should be refused
    run_prompt_test('wp_prompts.json')

    #mixed, tiered content prompts, expected behavior is defined in the json file
    run_prompt_test('tiered_prompts.json')
    
    
if __name__ == '__main__':
    main()

