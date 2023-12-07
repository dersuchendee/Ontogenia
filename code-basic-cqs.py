import pandas as pd
import openai
import logging
from datetime import datetime
openai.api_key = 'APIKEY'

logging.basicConfig(filename='ontology_design.log', level=logging.INFO)


def read_procedure(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Function to read CQs from a CSV file and optionally split them into groups
def read_and_split_CQs(file_path, split_into_groups=False):
    data = pd.read_csv(file_path)
    # Filter for CQs starting with 'awo_'
    awo_CQs = data[data['ID'].str.startswith('awo_')]['CQ'].tolist()

    if split_into_groups:
        # Splitting into 4 groups, adjust the logic as needed
        group_size = len(awo_CQs) // 4
        return [awo_CQs[i:i + group_size] for i in range(0, len(awo_CQs), group_size)]
    else:
        return awo_CQs

def generate_prompt(CQs, procedure="", combined_patterns="", previous_output=""):
    return (
        f"Read the following instructions: '{procedure}'. Basing on the procedure, and following the previous output: '{previous_output}',  design an ontology that comprehensively answers the following competency questions: '{CQs}', using the following ontology design patterns: {combined_patterns}. Do not repeat classes, object properties, data properties, restrictions, etc. if they have been addressed in the previous output. When you're done send me only the whole ontology you've designed in OWL format, without any comment outside the OWL."
    )

def design_ontology(prompt):
    messages = [
        {"role": "system", "content": "Follow the given examples and instructions and design the ontology"},
        {"role": "user", "content": prompt},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=messages,
        temperature=0,
        max_tokens=4096,
        frequency_penalty=0.0
    )

    logging.info(f"Response at {datetime.now()}: {response.choices[0].message['content'].strip()}")
    return response.choices[0].message['content'].strip(), response.usage.total_tokens

def main(CQs, procedure=None, combined_patterns=None, iteration=1):
    total_tokens_used = 0
    previous_output = ""  # Reset previous output for each trial

    # Determine if CQs are specific to awo
    is_awo_CQs = 'awo' in CQs[0][0]

    for group_number, CQs_group in enumerate(CQs, start=1):
        prompt = generate_prompt(CQs_group, procedure if procedure else "", combined_patterns if combined_patterns else "", previous_output)
        ontology_output, tokens_used = design_ontology(prompt)
        total_tokens_used += tokens_used
        previous_output += f"\n\n{ontology_output}"  # Carry over the output to the next group within the same trial
        logging.info(f"Group {group_number} processed. Tokens used: {tokens_used}. Total tokens used: {total_tokens_used}")

    # Generate dynamic file name
    date_str = datetime.now().strftime("%Y%m%d")
    case_str = 'awo' if is_awo_CQs else 'general'
    output_file_name = f"output_{case_str}_{date_str}_trial{iteration}.owl"

    output_path = f'outputs/{output_file_name}'
    with open(output_path, 'w') as file:
        file.write(previous_output)
    print(f"Ontology written to {output_path}. Total tokens used: {total_tokens_used}")

    return previous_output

if __name__ == "__main__":
    # Reading the procedure and patterns from files
    procedure_content = read_procedure('data/procedure.txt')
    pattern_data = pd.read_csv('data/patterns.csv')
    combined_pattern_str = '. '.join([f"{row['Name']}: {row['Pattern_owl']}" for _, row in pattern_data.iterrows()])

    # Reading and splitting the CQs
    CQs = read_and_split_CQs('data/CQs.csv', split_into_groups=True)

    iteration = 5 #ricorda di cambiare

    # Trial 1: Only divided CQs
    #print("Starting Trial 1")
    #previous_output = main(CQs, iteration=iteration)
    #iteration += 1

    # Trial 2: CQs and combined patterns
    #print("\nStarting Trial 2")
    #previous_output = main(CQs, combined_patterns=combined_pattern_str, iteration=iteration)
    #iteration += 1

    # Trial 3: Procedure only
    print("\nStarting Trial 3")
    previous_output = main(CQs, procedure=procedure_content, iteration=iteration)
    iteration += 1

    # Trial 4: All arguments
    #print("\nStarting Trial 4")
    #main(CQs, procedure=procedure_content, combined_patterns=combined_pattern_str, iteration=iteration)


    #2.10 dollars
    #totale della giornata: 3,14 dollari
