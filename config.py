# CONFIG/ USER INPUT:

# RELATIVE PATH DIRECTORY TO CONSTRICT LLM MODEL 
# !!!! DO NOT GIVE ACESS TO FOLDERS THAT YOU DONT HAVE BACKED UP AND SAVED OR CONTAIN ANYTHING SENSITIVE
# ONLY GIVE ACCESS TO THE FOLDER NECESSARY 
# !!!! LLM HAS WRITE ACESS TO FILES SO DO NOT GIVE ACCESSS HAPHAZARDLY ONCE AGAIN!!!!
WORKING_DIR = "./calculator"      # relative path 

# !!! LLM MODEL SELECTION:
# Default is openrouter.ai Free LLM MOdel rotation
LLM_MODEL = "openrouter/free"

# !!! LLM MODEL BEHAVIOR
"""
The recommended LLM (Large Language Model) temperature depends on your specific task, typically ranging from 0.0 to 1.0 (with some APIs scaling up to 2.0).
Recommended Settings by Task
• 0.0 – 0.2 (Deterministic & Factual): Best for data extraction, code generation, math, technical documentation, and Retrieval-Augmented Generation (RAG) where accuracy and consistency matter most.
• 0.3 – 0.6 (Balanced & Professional): Best for general-purpose chatbots, customer support, standard Q&A, and professional writing that needs a steady, natural tone.
• 0.7 – 1.0 (Creative & Exploratory): Best for brainstorming, creative writing, poetry, marketing copy, and open-ended ideation where variety and novelty are desired.
• Above 1.0 (High Randomness): Generally discouraged unless you want experimental or chaotic outputs, as values too high risk incoherence

Task Type	Recommended Temperature	         Why
Coding / SQL / Math	0.0 to 0.2	Forces the model to pick the single most logical, predictable token.
Factual Summarization / RAG	0.2 to 0.4	Reduces hallucinations and sticks strictly to source data.
General Chat / Assistants	0.5 to 0.7	Balances helpful structure with a natural conversational flow.
Creative Writing / Brainstorming	0.7 to 1.0	Flattens the probability curve to surface imaginative or unexpected words.
"""

LLM_MODEL_TEMPERATURE: float|int = 0



# CONSTANTS

## LIMITS

### LLM AGENT LOOP ITERATION LIMITS:
AGENT_LOOP_ITERATION_LIMIT = 20


### CHARACTER LIMITS:
LLM_Read_Characater_Limit = 10000


### CODE FILE EXECUTION LIMITS:

Py_File_Execution_Time_Limit = 30 # in seconds 

