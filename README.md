The model of AI-workflow that collects messages from different sources, examines them and creates a json-output with scoring of relevence.

##How to use:
1. Add your Anthropic api_key to the .env
2. Run python workflow.py

##Requirements:
-anthropic
-python-dotenv

##Descriptions:
workflow.py - the main file of the AI-workflow. Adds the context for an AI-model and the initial data about incident from the config.py.
First step: the model read the alert message and extract properties to filter the messages from different sources (Jira tickets, status pages etc)
Second step: the script call the collect() from info_collector.py
Third step: info_collector returns the json with mocked messages filtered by time
Fourth step: the second call of the model with analisyng prompt to look into the info_collectors output
Fifth step: the model returns a list of entities with scoring sorted by high to low score depending on time, sense and relativeness to the incident

logs.json - the log file
info_collector_output.mock.json - the mocked output for the info_collector
config.py - contains variables that could be changed