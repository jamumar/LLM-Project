import os
import openai
import json
from typing import List, Tuple
from models import Entity
from config import OPENAI_API_KEY
from transformers import pipeline

# Initialize the OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Load Hugging Face NER pipeline
ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", aggregation_strategy="simple")

async def extract_entities(text: str) -> Tuple[List[Entity], List[Entity]]:
    """Extract named entities using OpenAI and Hugging Face models."""
    
    # OpenAI NER
    try:
        openai_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a named entity recognition system. Identify entities and their types in the given text. Respond with a JSON array of objects, each containing 'entity' and 'type' keys."},
                {"role": "user", "content": text}
            ]
        )
        
        # Parse OpenAI response and extract entities
        openai_response_content = openai_response.choices[0].message.content
        openai_entities = parse_openai_response(openai_response_content) if openai_response_content else []
    except Exception as e:
        print(f"Error in OpenAI API call: {str(e)}")
        openai_entities = []

    # Hugging Face NER
    hf_entities = extract_entities_with_huggingface(text)

    return openai_entities, hf_entities

def parse_openai_response(response: str) -> List[Entity]:
    """Parses the OpenAI JSON response and returns a list of Entity objects."""
    try:
        entities_data = json.loads(response)
        return [Entity(**entity) for entity in entities_data]
    except json.JSONDecodeError:
        print(f"Failed to parse OpenAI response: {response}")
        return []

def extract_entities_with_huggingface(text: str) -> List[Entity]:
    """Uses Hugging Face NER model to extract named entities and groups subwords."""
    
    hf_results = ner_pipeline(text)

    entities = []
    for result in hf_results:
        entity_text = result["word"]
        entity_type = result["entity_group"]  # Uses grouped entity names

        entities.append(Entity(entity=entity_text, type=entity_type))

    return entities
