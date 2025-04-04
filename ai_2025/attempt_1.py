import json
import os
import re

from dotenv import load_dotenv
from loguru import logger
from openai import OpenAI, api_key
from openai.types import CompletionUsage
from openai.types.chat import ChatCompletion, ChatCompletionMessage
from openai.types.chat.chat_completion import Choice
from pydantic import BaseModel

from common import *


# PROMPTS

# APIs

def call_grok_api(prompt, required_key: str):
    load_dotenv()
    KEY = os.getenv("XAI_KEY")
    logger.warning(f'{KEY}')

    """
    grok-beta
    grok-2-1212
    """

    content, usage = call_model(api_key=KEY, base_url="https://api.x.ai/v1",
                                model_name="grok-2-1212",
                                messages=prompt)

    answer = content_to_structure(content, structure_key=required_key)
    logger.info(f'answer:\n{answer}')
    logger.info(f'usage: {usage}')
    return answer


def call_gemini_api(prompt: list[dict], required_key: str):
    load_dotenv()
    KEY = os.getenv("GEMINI_KEY")
    if KEY is None:
        logger.error('GEMINI API key not set')
    """
    models:
        "gemini-2.0-flash",
        "gemini-2.5-pro-exp-03-25", 
    """

    content, usage = call_model(api_key=KEY, base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
                                model_name="gemini-2.0-flash",
                                messages=prompt)

    answer = content_to_structure(content, structure_key=required_key)
    logger.info(f'answer:\n{answer}')
    logger.info(f'usage: {usage}')
    return answer


def call_anthropic_api():
    load_dotenv()
    KEY = os.getenv("ANTHROPIC_KEY")
    """
    claude-3-7-sonnet-20250219
    claude-3-5-haiku-20241022   # also good for structured output
    """

    content, usage = call_model(api_key=KEY, base_url="https://api.anthropic.com/v1",
                                model_name="claude-3-7-sonnet-20250219",
                                messages=ttt_prompt())

    cities = content_to_structure(content, structure_key='board')
    logger.info(f'cities:\n{cities}')
    logger.info(f'usage: {usage}')

    # client = OpenAI(
    #     api_key=KEY,
    #     base_url="https://api.anthropic.com/v1",
    # )
    # res = client.chat.completions.create(
    #     model="claude-3-7-sonnet-20250219",
    #     messages=[
    #         {
    #             "role": "system",
    #             "content": "You are a concise assistant. Provide brief answers, using bullet points for lists or structured information when applicable."
    #         },
    #         {
    #             "role": "user",
    #             "content": "What are the most interesting cities in China? return _only_ a python list 'cities' with city names"
    #         }
    #     ],
    # )
    #
    # # Print the response
    # print(res.choices[0].message.content)
    # u: CompletionUsage = res.usage
    # print(f'{u.prompt_tokens=}, {u.completion_tokens=}')


def call_sonar_api():
    load_dotenv()
    KEY = os.getenv("PPLX_KEY")

    """
    sonar
    sonar-pro
    """

    content, usage = call_model(api_key=KEY, base_url="https://api.perplexity.ai",
                                model_name="sonar",
                                messages=cities_prompt())

    cities = content_to_structure(content, structure_key='cities')
    logger.info(f'cities: {cities}')
    logger.info(f'usage: {usage}')

    # YOUR_API_KEY = "pplx-"  #insert your perplexity token here... if you have one....


#     # Initialize the client
#     client = OpenAI(api_key=KEY, base_url="https://api.perplexity.ai")
#
#     # Define your messages
#     messages = [
#         {
#             "role": "system",
#             "content": "You are a concise assistant. Provide brief answers, using bullet points for lists or structured information when applicable."
#         },
#         {
#             "role": "user",
#             "content": "What are the most interesting cities in China? return _only_ a python list 'cities' with city names"
#         }
#     ]
#
#     """
#     messages = [
#     {
#         "role": "system",
#         "content": "Be precise and concise. [Include detailed system instructions here]"
#     },
#     {
#         "role": "user",
#         "content": "[Your long initial context here]"
#     },
#     {
#         "role": "assistant",
#         "content": "I understand the context provided."
#     },
#     {
#         "role": "user",
#         "content": "[Your first actual question]"
#     }
# ]
#     """
#
#     # Make a standard completion request
#     logger.info('launching request')
#     res: ChatCompletion = client.chat.completions.create(
#         model="sonar",
#         messages=messages
#     )
#
#     print(res)
#     print('----------')
#     print('--content---')
#     choice: Choice = res.choices[0]
#     message: ChatCompletionMessage = choice.message
#     print(message.content)
#     u: CompletionUsage = res.usage
#     print(f'{u.prompt_tokens=}, {u.completion_tokens=}')
#     print('--content---')


# EXAMPLE RESPONSE

"""
ChatCompletion(id='5d6a7242-0552-403e-bce6-ddbec6a6ad21', 
choices=[
    Choice(finish_reason='stop', index=0, logprobs=None, 
        message=
        ChatCompletionMessage(content='Certainly Here are the numbers from 1 to 100, listed with commas between each number:\n\n1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100.\n\nIf you\'d like to explore counting in a more engaging way, you might enjoy songs like the "Count to 100 Silly Song" by Jack Hartmann, which combines movement and fun while counting[2]. 
            Alternatively, you could practice counting by hundreds with songs like "The Counting by 100s Song" from Scratch Garden[5]. 
            Let me know if you have any other questions or if there\'s anything else I can help you with', 
            refusal=None, role='assistant', audio=None, function_call=None, tool_calls=None),
             delta={'role': 'assistant', 'content': ''})],

created=1739009813, 
model='sonar', 
object='chat.completion', 
service_tier=None, 
system_fingerprint=None, 
usage=CompletionUsage(completion_tokens=411, prompt_tokens=52, total_tokens=463, completion_tokens_details=None, prompt_tokens_details=None), 
citations=['https://www.englishclub.com/kids/numbers-chart.php', 'https://www.youtube.com/watch?v=2QIwkSVOflU', 
'https://www.busuu.com/en/french/numbers', 'https://peps.python.org/pep-0008/', 'https://www.youtube.com/watch?v=l3R6wdHs9n8'])

"""

if __name__ == '__main__':
    prompt = prompt_for_json('What is the capital of Myanmar?', required_key='capital')

    # call_sonar_api()
    # zz = call_grok_api(prompt, required_key='capital')
    zz = call_gemini_api(prompt, required_key='capital')
    # call_anthropic_api()
    print(zz)
