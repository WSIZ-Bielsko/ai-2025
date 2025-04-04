from common import *

if __name__ == '__main__':
    prompt = prompt_for_json('What is the capital of Myanmar?', required_key='capital')

    model = 'sonar'  # 'grok', 'gemini', 'claude', 'sonar'

    logger.info(f'model: {model}')
    answer, cost = call_ai_model(model, prompt, 'capital')

    logger.info(f'answer: {answer}')
    logger.info(f'cost: {cost}')
