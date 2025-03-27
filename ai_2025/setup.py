import os

from dotenv import load_dotenv
from loguru import logger


def load_var():
    load_dotenv()
    key = os.getenv('XAI_KEY')
    logger.info(f'using {key=}')


if __name__ == '__main__':
    load_var()
