import os
import openai
import json
import re
import logging
from typing import List, Tuple
from models import Entity
from config import OPENAI_API_KEY
from transformers import pipeline
from dateutil import parser as date_parser

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize the OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Load Hugging Face NER pipeline
ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", aggregation_strategy="simple")

async def extract_entities(text: str) -> Tuple[List[Entity], List[Entity]]:
    """Extract named entities using OpenAI and Hugging Face models."""
    
    # OpenAI NER
    try:
        logger.info("Sending request to OpenAI API")
        openai_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a named entity recognition system. Identify entities and their types in the given text. Pay special attention to dates in various formats. Respond with a JSON array of objects, each containing 'entity' and 'type' keys. Use 'DATE' as the type for any date entities."},
                {"role": "user", "content": text}
            ]
        )
        
        # Log raw OpenAI response
        logger.debug(f"Raw OpenAI response: {openai_response}")
        
        openai_response_content = openai_response.choices[0].message.content
        logger.info(f"OpenAI response content: {openai_response_content}")
        
        # Parse OpenAI response and extract entities
        openai_entities = parse_openai_response(openai_response_content) if openai_response_content else []
        logger.info(f"Parsed OpenAI entities: {openai_entities}")
    except Exception as e:
        logger.error(f"Error in OpenAI API call: {str(e)}", exc_info=True)
        openai_entities = []

    # Hugging Face NER
    hf_entities = extract_entities_with_huggingface(text)
    logger.info(f"Hugging Face entities: {hf_entities}")

    return openai_entities, hf_entities

def parse_openai_response(response: str) -> List[Entity]:
    """Parses the OpenAI JSON response and returns a list of Entity objects."""
    try:
        # Remove any leading/trailing whitespace and newlines
        response = response.strip()
        logger.debug(f"Stripped response: {response}")
        
        # Check if the response is already a valid JSON string
        if response.startswith('[') and response.endswith(']'):
            logger.debug("Response appears to be a JSON array")
            entities_data = json.loads(response)
        else:
            logger.debug("Response is not a JSON array, attempting to extract JSON")
            # If not, try to extract JSON from a code block
            json_match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                logger.debug(f"Extracted JSON string: {json_str}")
                entities_data = json.loads(json_str)
            else:
                raise ValueError("Unable to extract JSON from the response")

        logger.info(f"Parsed entities data: {entities_data}")
        
        # Process entities, with special handling for dates
        processed_entities = []
        for entity in entities_data:
            if entity['type'].upper() == 'DATE':
                try:
                    # Attempt to parse the date
                    parsed_date = date_parser.parse(entity['entity'])
                    # Format the date consistently
                    entity['entity'] = parsed_date.strftime("%Y-%m-%d")
                except ValueError:
                    # If date parsing fails, keep the original string
                    logger.warning(f"Failed to parse date: {entity['entity']}")
            processed_entities.append(Entity(**entity))
        
        return processed_entities
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse OpenAI response: {response}")
        logger.error(f"JSON decode error: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Error parsing OpenAI response: {str(e)}")
        logger.error(f"Response: {response}")
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
