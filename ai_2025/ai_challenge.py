from loguru import logger
from pydantic import BaseModel

from ai_2025.common import prompt_for_json, call_ai_model, AI_MODELS


class AiChallengeScore(BaseModel):
    score: int  # 0/1
    format_error: int  # 0/1


def challenge_1(model: str) -> AiChallengeScore:
    prompt = prompt_for_json('What is the capital of Myanmar?', required_key='capital')
    try:
        answer, usage = call_ai_model(model, prompt, 'capital')
        logger.info(f'answer: {answer}')
        logger.info(f'cost: {usage}')
        return AiChallengeScore(score=1 if (answer == 'Naypyidaw') else 0, format_error=0)
    except Exception as e:
        logger.error(e)
        return AiChallengeScore(score=0, format_error=1)


def challenge_2(model: str) -> AiChallengeScore:
    prompt = prompt_for_json('if a<b and c<d is it always true, that a-d < b-c ?', required_key='answer')
    try:
        answer, usage = call_ai_model(model, prompt, 'answer')
        logger.info(f'answer: {answer}')
        logger.info(f'cost: {usage}')
        return AiChallengeScore(score=1 if (answer == 'Yes') else 0, format_error=0)
    except Exception as e:
        logger.error(e)
        return AiChallengeScore(score=0, format_error=1)


if __name__ == '__main__':
    # model = 'sonar'  # 'grok', 'gemini', 'claude', 'sonar'
    # model = 'grok'
    model = 'gemini'

    for model in AI_MODELS.keys():
        logger.warning(f'challenging {model}')
        x = challenge_2(model)
        print(x)
