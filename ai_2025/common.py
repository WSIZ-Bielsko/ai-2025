import json
import os
import re

from dotenv import load_dotenv
from loguru import logger
from openai import OpenAI
from openai.types import CompletionUsage
from pydantic import BaseModel


# MODEL


class AI_Model(BaseModel):
    name: str
    model_name: str
    base_url: str
    key_name: str


class CallCost(BaseModel):
    prompt_tokens: int
    completion_tokens: int

    @staticmethod
    def from_response(response):
        u: CompletionUsage = response.usage
        return CallCost(prompt_tokens=u.prompt_tokens, completion_tokens=u.completion_tokens)


AI_MODELS: dict[str, AI_Model] = {
    "gemini": AI_Model(
        name="gemini",
        model_name="gemini-2.0-flash",
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        key_name="GEMINI_KEY"
    ),
    "grok": AI_Model(
        name="grok",
        base_url="https://api.x.ai/v1",
        model_name="grok-2-1212",
        key_name="XAI_KEY"
    ),
    "sonar": AI_Model(
        name="sonar",
        base_url="https://api.perplexity.ai",
        model_name="sonar",
        key_name="PPLX_KEY"
    ),
    "claude": AI_Model(
        name="claude",
        base_url="https://api.anthropic.com/v1",
        model_name="claude-3-7-sonnet-20250219",
        key_name="ANTHROPIC_KEY"
    )
}




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


def call_ai_model(model_name: str, prompt: list[dict], required_key: str):
    load_dotenv()

    config = AI_MODELS[model_name]
    key = os.getenv(config.key_name)

    content, usage = call_model(
        api_key=key,
        base_url=config.base_url,
        model_name=config.model_name,
        messages=prompt
    )

    answer = content_to_structure(content, structure_key=required_key)
    return answer, usage


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
