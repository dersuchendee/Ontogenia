# Ontogenia

## Overview
Ontogenia is a Python-based project focused on exploring ontology generation and management. This repository includes scripts and data essential for conducting complex query solutions and thematic ontology constructions.

## Repository Structure
- **code-basic-cqs.py**: Script for basic complex queries.
- **code-thematic-cqs.py**: Script for thematic complex queries.
- **data/**: Contains data files used in ontology processes.
- **outputs/**: Stores outputs from the scripts.
- **ontology_design.log**: Logs details of the ontology design process experiments.
- **thematic_groups.json**: JSON file containing thematic groups information.

### code-basic-cqs.py
# Ontogenia Python Script Overview

#### Overview
This script is designed to automate ontology generation by integrating OpenAI's language model, data handling with pandas, and detailed logging. It facilitates the reading, processing, and application of competency questions (CQs) to generate ontologies using specific patterns and procedures.

#### Key Components
- **Data Reading**: Scripts read procedure texts and CQs from specified files.
- **Ontology Generation**: Utilizes OpenAI's API to generate ontologies based on the CQs provided, with the capability to split questions into groups for detailed processing.
- **Logging**: Tracks the process and outcomes of ontology generation using the `logging` module, saving logs to 'ontology_design.log'.
- **Output Management**: Outputs are written to .owl files, named dynamically based on the date and specifics of the CQs processed.

#### Workflow
1. **Initialize**: Read the procedure and patterns from text and CSV files.
2. **Process CQs**: Optionally split CQs into thematic groups.
3. **Generate Ontologies**: Create prompts from CQs, invoke the LLM to generate ontology sections, and log the responses.
4. **Compile and Save**: Concatenate generated ontology sections, save them in a structured OWL format file, and log the total token usage and process details.

#### Usage
To run the script, simply execute the main function with the desired settings for trial iterations and data paths. The script can handle different configurations such as only CQs, CQs with patterns, or procedure-based generation to accommodate various experimental setups.


## How to Use
1. Clone the repository.
2. Ensure Python is installed on your machine.
3. Run the scripts to perform ontology generation tasks.

## Contributing
Contributions are welcome. Please open an issue to discuss your ideas or submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
