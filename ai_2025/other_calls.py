from loguru import logger

from ai_2025.common import prompt_for_json, call_ai_model, AI_MODELS

if __name__ == '__main__':
    prompt = prompt_for_json("what happens if os.getenv(envvar) is called in python, and the envvar is not set", required_key='answer')
    try:
        answer, usage = call_ai_model('gemini-simple', prompt, 'answer')
        logger.info(f'answer: {answer}')
        logger.info(f'cost: {usage}')
    except Exception as e:
        logger.error(e)


