from loguru import logger

from ai_2025.common import prompt_for_json, call_ai_model, AI_MODELS

if __name__ == '__main__':
    prompt = prompt_for_json('Create a python list of 12 main personality traits (psychology)', required_key='traits')
    try:
        answer, usage = call_ai_model('qwen', prompt, 'traits')
        logger.info(f'answer: {answer}')
        logger.info(f'cost: {usage}')
    except Exception as e:
        logger.error(e)


