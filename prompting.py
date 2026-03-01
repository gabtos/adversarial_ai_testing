import json
import re
from pathlib import Path
from datetime import datetime
from ollama import chat
from defense import safe_generate


# requires ollama to be installed and running
# remember to run 'brew services start ollama' 
# then run 'ollama run llama3.2' in a separate terminal 

def generate_responses(prompt_file: str, model_name: str = "llama3.2"):
    # ----------------------------
    # Load prompt suite
    # ----------------------------
    with open(prompt_file, 'r', encoding='utf-8') as f:
        prompts = json.load(f)

    # ----------------------------
    # Add run metadata
    # ----------------------------
    run_timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S_UTC")

    results = {
        "run_metadata": {
            "timestamp_utc": run_timestamp,
            "model": model_name,
            "source_prompt_file": prompt_file
        },
        "prompts": []
    }

    # ----------------------------
    # Run prompts
    # ----------------------------
    for case in prompts["prompts"]:

        response = chat(
            model=model_name,
            messages=[
                {"role": "user", "content": case["prompt"]}
            ],
        )

        output_text = response.message.content

        print(f"\n--- {case['id']} ---")
        print(output_text)

        # Copy original case + response into results
        result_case = case.copy()
        result_case["response"] = output_text

        # results["prompts"].append(result_case)

    # ----------------------------
    # Create results directory
    # ----------------------------
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    # Create filename with timestamp
    base_name = Path(prompt_file).stem
    output_filename = f"safe_{base_name}_{model_name}_{run_timestamp}.json"
    output_path = results_dir / output_filename

    # ----------------------------
    # Save results file
    # ----------------------------
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)

    print(f"\nSaved results to: {output_path}")

    return output_path

def main():
    
    # #violent content prompts, all should be refused
    # generate_responses('vt_prompts.json')

    # #weapon content prompts, all should be refused
    # generate_responses('wp_prompts.json')

    # #mixed, tiered content prompts, expected behavior is defined in the json file
    # generate_responses('tiered_prompts.json')

    #testing safe generation
    safe_generate('vt_prompts.json')
    safe_generate('tiered_prompts.json')
    safe_generate('wp_prompts.json')
    
    
if __name__ == '__main__':
    main()

