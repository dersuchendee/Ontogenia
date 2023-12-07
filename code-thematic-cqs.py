import pandas as pd
import openai
import logging
from datetime import datetime
openai.api_key = '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'

logging.basicConfig(filename='ontology_design.log', level=logging.INFO)


def read_procedure(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Function to read CQs from a CSV file and optionally split them into groups

import re

# Function to split a string of CQs into groups
def split_CQs_from_string(cq_string, split_into_groups=True):
    # Split the string into thematic groups using '**' as delimiters
    thematic_groups = re.split(r'\*\*[^*]+\*\*', cq_string)
    # Remove any empty strings that may have resulted from the split
    thematic_groups = [group.strip() for group in thematic_groups if group.strip()]

    # Split each thematic group into individual CQs
    thematic_grouped_CQs = []
    for group in thematic_groups:
        # Split the group into individual CQs using a regex that looks for numbers followed by '.'
        cq_list = re.split(r'\d+\.\s*', group)
        # Remove any empty strings that may have resulted from the split
        cq_list = [cq for cq in cq_list if cq]
        thematic_grouped_CQs.append(cq_list)

    print(thematic_grouped_CQs)
    return thematic_grouped_CQs

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
    cumulative_output = ""  # Initialize cumulative output for the entire trial

    for group_number, CQs_group in enumerate(CQs, start=1):
        # Generate prompt for the current group, including all previous outputs
        prompt = generate_prompt(CQs_group, procedure if procedure else "", combined_patterns if combined_patterns else "", cumulative_output)
        ontology_output, tokens_used = design_ontology(prompt)
        total_tokens_used += tokens_used

        # Update cumulative output with the current group's output
        cumulative_output += f"\n\n{ontology_output}"  # Append current group output for the next group

        logging.info(f"Group {group_number} processed. Tokens used: {tokens_used}. Total tokens used: {total_tokens_used}")

    # Generate dynamic file name
    date_str = datetime.now().strftime("%Y%m%d")
    output_file_name = f"output_trial{iteration}_{date_str}.owl"

    output_path = f'outputs/{output_file_name}'
    with open(output_path, 'w') as file:
        file.write(cumulative_output)
    print(f"Ontology written to {output_path}. Total tokens used: {total_tokens_used}")

    return cumulative_output

if __name__ == "__main__":
    # Reading the procedure and patterns from files
    procedure_content = read_procedure('data/procedure.txt')
    pattern_data = pd.read_csv('data/patterns.csv')
    combined_pattern_str = '. '.join([f"{row['Name']}: {row['Pattern_owl']}" for _, row in pattern_data.iterrows()])

    # Reading and splitting the CQs
    #CQs = read_and_split_CQs('data/CQs.csv', split_into_groups=True)
    cq_string = "The competency questions can be divided into thematic groups as follows:**Diet and Feeding Habits** 1. Which animal eats which other animal? 2. Is [this animal] a herbivore? 3. Which plant parts does [this omnivorous or herbivorous animal] eat? 4. Does a lion eat plants or plant parts? 5. Which plants eat animals? 6. Which animals eat [these animals]? 7. Which animals are the predators of [these animals]? 8. Is there an animal that does not drink water? 9. Are there animals that are carnivore but still eat some plants or parts of plants? **Geographical Distribution and Habitat** 10. Are there [these animals] in [this country]? 11. Which country do I have to visit to see [these animals]? 12. In what kind of habitat do [this animal] live? 13. Do [this animal] and [this animal] live in the same habitat? **Conservation Status** 14. Which animals are endangered? These thematic groups help organize the ontology around key concepts such as diet, habitat, geographical distribution, and conservation status."
    CQs = split_CQs_from_string(cq_string)
    print(CQs)

    iteration = 1

    # Trial 1: Only divided CQs
    print("Starting Trial 1")
    previous_output = main(CQs, iteration=iteration)

    iteration += 1

    # Trial 2: CQs and combined patterns
    print("\nStarting Trial 2")
    previous_output = main(CQs, combined_patterns=combined_pattern_str, iteration=iteration)
    iteration += 1

    # Trial 3: Procedure only
    print("\nStarting Trial 3")
    previous_output = main(CQs, procedure=procedure_content, iteration=iteration)
    iteration += 1

    # Trial 4: All arguments
    print("\nStarting Trial 4")
    main(CQs, procedure=procedure_content, combined_patterns=combined_pattern_str, iteration=iteration)


    #2.10 dollars
    #totale della giornata: 3,14 dollari