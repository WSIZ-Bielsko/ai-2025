import json
import re

from loguru import logger
from openai import OpenAI
from openai.types import CompletionUsage
from pydantic import BaseModel


# MODEL


class CallCost(BaseModel):
    prompt_tokens: int
    completion_tokens: int

    @staticmethod
    def from_response(response):
        u: CompletionUsage = response.usage
        return CallCost(prompt_tokens=u.prompt_tokens, completion_tokens=u.completion_tokens)


# HELPERS


def call_model(api_key: str, base_url: str, model_name: str, messages: list[dict]) -> tuple[str, CallCost]:
    client = OpenAI(api_key=api_key, base_url=base_url)
    logger.info(f'calling {model_name}')
    # .....
    res = client.chat.completions.create(model=model_name, messages=messages)
    content = res.choices[0].message.content
    cost = CallCost.from_response(res)
    return content, cost


def content_to_structure(content: str, structure_key: str = 'answer'):
    cleaned_content = re.sub(r'```json\s*|\s*```', '', content).strip()
    try:
        xx = json.loads(cleaned_content)
    except ValueError:
        logger.error(f'not json-parseable: {content}')
        raise RuntimeError('Error parsing JSON')
    try:
        answer = xx[structure_key]
    except KeyError:
        logger.error(f'structure key {structure_key} not found in answer')
        raise RuntimeError(f'structure key {structure_key} not found in answer')
    return answer


# PROMPTS

def cities_prompt():
    messages = [
        {
            "role": "system",
            "content": "You are a concise assistant. Provide responses in a structured JSON format. "
                       "Return only a JSON object with proper keys"
        },
        {
            "role": "user",
            "content": "What are the most interesting cities in China? return _only_ a python object with key 'cities' containing the list with city names"
        }
    ]
    return messages


def ttt_prompt() -> list[dict]:
    messages = [
        {
            "role": "system",
            "content": "You are a concise assistant. Provide responses in a structured JSON format. "
                       "Return only a JSON object with proper keys"
        },
        {
            "role": "user",
            "content": """The following tic-tac-toe board is given:
.o.
.x.
...

next move is 'x', and it is your move, make a good move, print the board after the move. Return _only_ the  json structure with key "board". """
        }
    ]
    return messages


def prompt_for_json(message: str, required_key: str) -> list[dict]:
    messages = [
        {
            "role": "system",
            "content": "You are a concise assistant. Provide responses in a structured JSON format. "
                       "Return only a JSON object with proper keys"
        },
        {
            "role": "user",
            "content": message + f". Return _only_ the  json structure with key `{required_key}`. "
        }
    ]
    return messages
